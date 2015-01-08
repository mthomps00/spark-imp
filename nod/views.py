from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from rsvp.models import Camp, SparkProfile, Invitation
from nod.models import *
import re

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
    nominations = Nomination.objects.filter(camp=camp).order_by('user')
    ballot, created = Ballot.objects.get_or_create(voter=request.user, voting_round=current_round)
    num_votes = current_round.num_votes
    
    if request.method == 'POST':
        tally = request.POST.getlist('vote_tally')
        nominees = request.POST.getlist('voter_id')
        h = 0
        i = len(nominees)
        while h < i:
            value = tally[h]
            nod = Nomination.objects.get(id=nominees[h])
            vote, created = Vote.objects.get_or_create(user=nod.user, ballot=ballot)
            if created == False:
                vote.value = value
                vote.save()
            h += 1

    for nomination in nominations:
        count = 0
        nomination.allvotes = Vote.objects.filter(user=nomination.user)
        nomination.othernods = Nomination.objects.filter(user=nomination.user, camp=camp).exclude(pk=nomination.pk)
        your_vote, created = Vote.objects.get_or_create(user=nomination.user, ballot=ballot)
        for vote in nomination.allvotes:
            count = count + vote.value
        nomination.count = count
        nomination.minimum = count - your_vote.value
        
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