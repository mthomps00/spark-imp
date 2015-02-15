from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, RequestContext
from django.template.defaultfilters import slugify
from rsvp.models import Camp, SparkProfile, Invitation
from nod.models import *
from nod.forms import *
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

def nominate(request, camptheme=''):
    if request.method == 'POST':
        form = NominationForm(request.POST)

        if form.is_valid():
            user_first_name = form.cleaned_data['user_first_name']
            user_last_name = form.cleaned_data['user_last_name']
            user_email = form.cleaned_data['user_email']
            user_alum = form.cleaned_data['user_alum']
            reason = form.cleaned_data['reason']
            description = form.cleaned_data['description']
            employer = form.cleaned_data['employer']
            job_title = form.cleaned_data['job_title']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            poc = form.cleaned_data['poc']
            camp = form.cleaned_data['camp']
            secondary_email = form.cleaned_data['secondary_email']
            
            if gender == 'F':
                woman = True
            else:
                woman = False
            
            comboname = user_first_name + user_last_name
            noddername = slugify(comboname)
            nominated_by, nodcreated = User.objects.get_or_create(username=noddername)

            if nodcreated:
                messages.success(request, 'Created nominator: ' + nominated_by.username)
            else:
                messages.success(request, 'Assigned nominated_by to existing user: ' + nominated_by.username)

            nodprof = SparkProfile.objects.get(user=nominated_by)
            nominated_by.first_name = user_first_name
            nominated_by.last_name = user_last_name
            nominated_by.email, nodprof.email = user_email, user_email
            nominated_by.save()
            nodprof.save()
            
            comboname = first_name + last_name
            username = slugify(comboname)
            user, usercreated = User.objects.get_or_create(username=username)

            if usercreated:
                messages.success(request, 'Created user: ' + user.username)
            else:
                messages.success(request, 'Created nomination for existing user: ' + user.username)

            prof = SparkProfile.objects.get(user=user)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email, email
            user.save()
            
            profile = SparkProfile.objects.get(user=user)
            profile.employer = employer
            profile.email = email
            profile.job_title = job_title
            profile.secondary_email = secondary_email
            profile.woman = woman
            if poc = True:
                profile.poc = True            
            profile.save()
            nomination, nodcreated = Nomination.objects.update_or_create(user=user, nominated_by=nominated_by, reason=reason, description=description)
            messages.success(request, 'Thank you for nominating someone for Spark Camp!')
            
            if camp != 'N':
                nomination.camp = Camp.objects.get(short_name=camp)
                nomination.save()

            userdata = {
                'user_first_name': user_first_name,
                'user_last_name': user_last_name,
                'user_email': user_email,
                'camp': camp,
            }
            form = NominationForm(initial=userdata)
    else:
        form = NominationForm()
            
    variables = {
        'form': form,
        'camptheme': camptheme,
    }
            
    return render_to_response('nod/nominate.html', variables, context_instance=RequestContext(request))

  
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
            if current_tally > 0:
                nod = Nomination.objects.get(id=nominees[h])
                vote, created = Vote.objects.get_or_create(user=nod.user, ballot=ballot)
                vote.value=current_tally
                vote.save()
            h += 1
        return redirect('round', round=round)

    for nomination in nominations:
        count = 0
        yours = 0
        nomination.othervotes = Vote.objects.filter(user=nomination.user, ballot__voting_round=round).exclude(ballot__voter=request.user)
        nomination.yourvotes = Vote.objects.filter(user=nomination.user, ballot=ballot)
        for vote in nomination.othervotes:
            count = count + vote.value
        for vote in nomination.yourvotes:
            yours = yours + vote.value
        nomination.count = count
        nomination.yours = yours
        
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
        pick.value = sum(Vote.objects.filter(user=pick.id,ballot__voting_round=round).values_list('value',flat=True))
    
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

        