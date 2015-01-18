from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, RequestContext
from rsvp.models import Camp, SparkProfile, Invitation
from nod.models import *
import re, datetime

####################
# SEARCH VIEWS
####################

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

@login_required
def search(request, nominate=False):
    query_string = ''
    results = None
    camps = Camp.objects.all()
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        item_query = get_query(query_string, ['last_name','first_name','username','sparkprofile__bio','sparkprofile__employer'])
        results = User.objects.filter(item_query).order_by('last_name')
        
    variables = {
        'query_string': query_string,
        'results': results,
        'nominate': nominate,
        'camps': camps,
    }
    
    return render_to_response('nod/search.html', variables, context_instance=RequestContext(request))

@login_required
def nominated(request, camp=False):
    if request.method == 'POST':
        nominees = request.POST.getlist('checked')
        selected_camp = request.POST.get('campselect')
        if selected_camp != '':
            camp = Camp.objects.get(id=selected_camp)
            
        nominations = []
        existing_nominations = []
        for nominee in nominees:
            user = User.objects.get(id=nominee)
            if camp:
                n, created = Nomination.objects.get_or_create(user=user, nominated_by=request.user, camp=camp)
            else:
                n, created = Nomination.objects.get_or_create(user=user, nominated_by=request.user)
            if created:
                nominations.append(n)
            else:
                existing_nominations.append(n)
                
        variables = {
            'nominate': True,
            'nominations': nominations,
            'existing_nominations': existing_nominations,
            'camp': camp,
        }
    return render_to_response('nod/nominated.html', variables, context_instance=RequestContext(request))

@login_required
def vote(request, round):
    current_round = VotingRound.objects.get(id=round)
    camp = Camp.objects.get(id=current_round.camp.id)
    nominations = Nomination.objects.filter(camp=camp).exclude(success=True).order_by('user')
    ballot, created = Ballot.objects.get_or_create(voter=request.user, voting_round=current_round)
    num_votes = current_round.num_votes
    
    if request.method == 'POST':
        tally = request.POST.getlist('vote_tally')
        nominees = request.POST.getlist('nominee_id')
        h = 0
        i = len(nominees)
        while h < i:
            current_tally = int(float(tally[h]))
            nod = Nomination.objects.get(id=nominees[h])
            votes = Vote.objects.filter(user=nod.user, ballot__voting_round=round).exclude(ballot=ballot).values_list('value', flat=True)
            votecount = sum(votes)
            value = current_tally - votecount
            vote, created = Vote.objects.get_or_create(user=nod.user, ballot=ballot)
            vote.value = value
            if value == 0:
                vote.delete()
            else:
                vote.save()
            h += 1
        return redirect('round', round=round)

    for nomination in nominations:
        count = 0
        nomination.votes = Vote.objects.filter(user=nomination.user)
        nomination.your_vote, created = Vote.objects.get_or_create(user=nomination.user, ballot=ballot)
        for vote in nomination.votes:
            count = count + vote.value
        nomination.count = count
        nomination.minimum = count - nomination.your_vote.value
        
    ballot_votes = Vote.objects.filter(ballot=ballot)
    vote_count = 0
    for vote in ballot_votes:
        vote_count = vote_count + vote.value
    num_votes = num_votes - vote_count
    
    variables = {
        'camp': camp,
        'nominations': nominations,
        'round': current_round,
        'num_votes': num_votes,
    }
    
    return render_to_response('nod/vote.html', variables, context_instance=RequestContext(request))

@login_required
def round(request, round):
    round = VotingRound.objects.get(id=round)
    ballot, created = Ballot.objects.get_or_create(voter=request.user, voting_round=round)
    votes = Vote.objects.filter(value__gt=0,ballot__voting_round=round)
    all_ids = votes.values_list('user',flat=True)
    all_picks = User.objects.filter(id__in=all_ids)
    your_ids = Vote.objects.filter(value__gt=0,ballot=ballot).values_list('user',flat=True)
    your_picks = User.objects.filter(id__in=your_ids)
    
    for pick in all_picks:
        pick.value = sum(Vote.objects.filter(user=pick.id).values_list('value',flat=True))
    
    # Calculate the demographic breakdown of the round.
    all_poc = all_picks.filter(sparkprofile__poc=True)
    your_poc = your_picks.filter(sparkprofile__poc=True)
    all_women = all_picks.filter(sparkprofile__woman=True)
    your_women = your_picks.filter(sparkprofile__woman=True)
    
    def percent(part, whole):
        denominator = float(len(whole))
        numerator = float(len(part))
        if denominator <= 0:
            denominator = 1
        return int(100 * (numerator/denominator))

    percents = {
        'poc': percent(all_poc, all_picks),
        'women': percent(all_women, all_picks),
        'your_poc': percent(your_poc, your_picks),
        'your_women': percent(your_women, your_picks),
        }
    
    variables = {
        'round': round,
        'all_picks': all_picks,
        'your_picks': your_picks,
        'ballot': ballot,
        'percents': percents,
    }
    
    return render_to_response('nod/round.html', variables, context_instance=RequestContext(request))
  
@login_required
def invites(request, camptheme):
    camp = Camp.objects.get(theme=camptheme)
    
    if request.method == 'POST':
        invitees = request.POST.getlist('invite')
        expires = request.POST.get('deadline')
        today = datetime.date.today()
    
        # Change the number of days in the following line to alter the RSVP response deadline for the new invitations.
        daysleft = timedelta(days=int(expires))
        expiration = today + daysleft

        for invitee in invitees:
            user = User.objects.get(id=invitee)
            invite, created = Invitation.objects.get_or_create(user=user,camp=camp)
            if created:
                Nomination.objects.filter(camp=camp,user=user).update(success=True)
                invite.expires = expiration
                if user.email:
                    invite.status = 'P'
                else:
                    invite.status = 'Q'
            invite.save()
    
    invitations = Invitation.objects.filter(camp=camp,status='P').order_by('user__last_name')
    emailless = Invitation.objects.filter(camp=camp,status='Q').order_by('user__last_name')
    
    variables = {
        'camp': camp,
        'invitations': invitations,
        'emailless': emailless,
    }
    
    return render_to_response('nod/invites.html', variables, context_instance=RequestContext(request))

@login_required
def process_emails(request):
    if request.method == 'POST':
        
        emails = request.POST.getlist('email')
        invitations = request.POST.getlist('invite_id')
        added = []
        
        for count, invitation in enumerate(invitations):
            invite = Invitation.objects.get(id=invitations[count])
            user = invite.user
            if emails[count] != '':
                user.email = emails[count]
                user.sparkprofile.email = emails[count]
                user.save()
                user.sparkprofile.save()
                
        request = added
        return render_to_response('nod/request.html', {'request': request }, context_instance=RequestContext(request))

        