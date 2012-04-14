from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render_to_response
from rsvp.models import *
from rsvp.forms import *
import random
from datetime import date

@login_required
def main_page(request):
    today = date.today()

    camps = Camp.objects.filter(start_date__gte=today)
    variables = {
        'camps' : camps,
    }
    return render_to_response('main.html', variables, context_instance=RequestContext(request))

@login_required
def user_page(request, username):
    user = get_object_or_404(User, username=username)        
    invitations = user.invitation_set.all()
    
    for invitation in invitations:
        invitation.status = invitation.get_status_display()
    
    variables = {
        'username': username,
        'invitations': invitations,
    }
    return render_to_response('users.html', variables, context_instance=RequestContext(request))

@login_required
def camps(request):
    try:
        camps = Camp.objects.all()
    except Camp.DoesNotExist:
        raise Http404(u'No camps have been created yet.')
    
    variables = {
        'camps': camps,
    }
    return render_to_response('camps.html', variables, context_instance=RequestContext(request))
    
@login_required
def single_camp(request, camptheme):
    try:
        camp = Camp.objects.get(theme__iexact=camptheme)
    except Camp.DoesNotExist:
        raise Http404(u'Could not find this Camp.')
    invitations = Invitation.objects.filter(camp=camp)
    for invitation in invitations:
        invitation.status = invitation.get_status_display()
        invitation.stipend = invitation.stipend_set.all()
        invitation.roommate = invitation.roommate_set.all()
        invitation.ignite = invitation.ignite_set.all()
        
    confirmed = invitations.filter(status='Y')
    confirmed_pocs = confirmed.filter(user__sparkprofile__poc=True)
    confirmed_women = confirmed.filter(user__sparkprofile__woman=True)
    confirmed_journos = confirmed.filter(user__sparkprofile__journo=True)
    
    def percent(part, whole):
        denominator = float(len(whole))
        numerator = float(len(part))
        if denominator <= 0:
            denominator = 1
        return int(100 * (numerator/denominator))
        
    percent_poc = percent(confirmed_pocs, confirmed)
    percent_women = percent(confirmed_women, confirmed)
    percent_journos = percent(confirmed_journos, confirmed)
    
    variables = {
        'camp': camp,
        'invitations': invitations,
        'confirmed': confirmed,
        'percent_poc': percent_poc,
        'percent_women': percent_women,
        'percent_journos': percent_journos,
    }
    return render_to_response('single_camp.html', variables, context_instance=RequestContext(request))

def guest_invite(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation.')       
    
    # Declare global variables
    today = date.today()
    update = False
    formvars = False
    detailform = InviteDetailForm()
    user = invitation.user
    
    def decideform(formvars={}):
        if invitation.status == 'Y':
            message = 'We\'re looking forward to your attendance at Spark Camp. We have you confirmed as coming. If your plans have changed, please use this form to let us know.'
            form = UpdateForm(formvars)
        elif invitation.expires < today:
            message = 'It\'s after the deadline (%s) for your invitation, but if it turns out you can make it to Spark Camp, we may still be able to accommodate you. Please let us know whether we should put you on the waitlist, and we\'ll be in touch very soon with an update.' % invitation.expires
            form = WaitlistForm(formvars)
        elif invitation.status == 'N' or invitation.status == 'C':
            message = 'We\'re sorry to hear you can\'t make it to Spark Camp. Please return here and let us know if your plans change in our favor.'
            form = ResurrectForm(formvars)  
        elif invitation.status == 'W':
            message = 'We have you on the waitlist for Spark Camp. Please let us know if it turns out you can\'t make it.'
            form = WaitlistForm(formvars)
        else:
            message = 'We very much hope you can make it to Spark Camp. Please use this form to submit your RSVP.'
            form = ResponseForm(formvars)
        return message, form

    if request.method == 'POST':
        message, form = decideform(request.POST)
        if form.is_valid():
            invitation.status = form.cleaned_data['status']
            invitation.save()
            message, form = decideform(request.POST)
            update = 'Thank you for updating your status.'
    else:
        message, form = decideform()
        
    # Find roommate requests
    if invitation.roommate_set.all():
        roommates = invitation.roommate_set.all()
        roommate = roommates[0]
        roommate.sex = roommate.get_sex_display()
        roommate.roommate = roommate.get_roommate_display()
    else:
        roommate = False
    
    # Find stipend requests
    if invitation.stipend_set.all():
        stipends = invitation.stipend_set.all()
        stipend = stipends[0]
        stipend.jobhelp = stipend.get_employer_subsidized_display()
    else:
        stipend = False
        
    # Find Ignite sign-ups
    if invitation.ignite_set.all():
        ignites = invitation.ignite_set.all()
        ignite = ignites[0]
        ignite.jobhelp = ignite.get_experience_display()
    else:
        ignite = False
    
    variables = {
        'invitation': invitation,
        'form': form,
        'detailform': detailform,
        'update': update,
        'message': message,
        'user': user,
        'roommate': roommate,
        'stipend': stipend,
        'ignite': ignite,
    }

    return render_to_response('single_invite.html', variables, context_instance=RequestContext(request))

def roommate(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation.')

    if request.method == 'POST':
        form = RoommateForm(request.POST)
        if form.is_valid():
            sex = form.cleaned_data['sex']
            roommate = form.cleaned_data['roommate']
            more = form.cleaned_data['more']
            newRoommate = Roommate(invitation=invitation, sex=sex, roommate=roommate, more=more)
            newRoommate.save()
            return HttpResponseRedirect('/rsvp/%s' % invitation.rand_id)
    else:
        form = RoommateForm()
    
    return render_to_response('roommate.html', { 'form': form, 'invitation': invitation, }, context_instance=RequestContext(request))
    
def ignite(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation.')

    if request.method == 'POST':
        form = IgniteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            experience = form.cleaned_data['experience']
            description = form.cleaned_data['description']
            newIgnite = Ignite(invitation=invitation, title=title, experience=experience, description=description)
            newIgnite.save()
            return HttpResponseRedirect('/rsvp/%s' % invitation.rand_id)
    else:
        form = IgniteForm()
    
    return render_to_response('ignite.html', { 'form': form, 'invitation': invitation, }, context_instance=RequestContext(request))
    
def stipend(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation.')

    if request.method == 'POST':
        form = StipendForm(request.POST)
        if form.is_valid():
            cost_estimate = form.cleaned_data['cost_estimate']
            employer_subsidized = form.cleaned_data['employer_subsidized']
            employer_percentage = form.cleaned_data['employer_percentage']
            invitee_percentage = form.cleaned_data['invitee_percentage']
            details = form.cleaned_data['details']
            newStipend = Stipend(invitation=invitation, cost_estimate=cost_estimate, employer_subsidized=employer_subsidized, employer_percentage=employer_percentage, invitee_percentage=invitee_percentage, details=details)
            newStipend.save()
            return HttpResponseRedirect('/rsvp/%s' % invitation.rand_id)
    else:
        form = StipendForm()
    
    return render_to_response('stipend.html', { 'form': form, 'invitation': invitation, }, context_instance=RequestContext(request))
    
def stipend_detail(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation, so no stipend.')

    if invitation.stipend_set.all():
        stipends = invitation.stipend_set.all()
        stipend = stipends[0]
        stipend.jobhelp = stipend.get_employer_subsidized_display()
    else:
        stipend = False
        
    variables = {
        'stipend': stipend,
        'invitation': invitation,
    }
    
    return render_to_response('stipend_detail.html', variables, context_instance=RequestContext(request))
    
def roommate_detail(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation, so no stipend.')

    if invitation.roommate_set.all():
        roommates = invitation.roommate_set.all()
        roommate = roommates[0]
        roommate.sex = roommate.get_sex_display()
        roommate.roommate = roommate.get_roommate_display()
    else:
        roommate = False
        
    variables = {
        'roommate': roommate,
        'invitation': invitation,
    }
    
    return render_to_response('roommate_detail.html', variables, context_instance=RequestContext(request))
    
def ignite_detail(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation, so no stipend.')

    if invitation.ignite_set.all():
        ignites = invitation.ignite_set.all()
        ignite = ignites[0]
        ignite.experience = ignite.get_experience_display()
    else:
        ignite = False
        
    variables = {
        'ignite': ignite,
        'invitation': invitation,
    }
    
    return render_to_response('ignite_detail.html', variables, context_instance=RequestContext(request))
    
def invite_logistics(request, rand_id):
    try:
        invitation = Invitation.objects.get(rand_id=rand_id)
    except Invitation.DoesNotExist:
        raise Http404(u'Could not find this Invitation.')

    if request.method == 'POST':
        form = InviteDetailForm(request.POST, instance=invitation)
        if form.is_valid():
            invitation.dietary = form.cleaned_data['dietary']
            invitation.arrival_time = form.cleaned_data['arrival_time']
            invitation.departure_time = form.cleaned_data['departure_time']
            invitation.hotel_booked = form.cleaned_data['hotel_booked']
            invitation.save()
    else:
        form = InviteDetailForm(instance=invitation)
    
    variables = {
        'invitation': invitation,
        'form': form,
    }
    
    return render_to_response('logistics.html', variables, context_instance=RequestContext(request))