# coding: utf-8

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import Context, RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render_to_response
from rsvp.models import *
from rsvp.forms import *
from rsvp.mailsnake import MailSnake
import random, csv, datetime
from datetime import date, timedelta
from urllib import urlopen

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
    camp = get_object_or_404(Camp, theme__iexact=camptheme)
    syncform = GoogleSyncForm()
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

@login_required
def dietary(request, camptheme):
    camp = get_object_or_404(Camp, theme__iexact=camptheme)
    invitations = Invitation.objects.filter(camp=camp).filter(status='Y')
    
    variables = {
        'camp': camp,
        'invitations': invitations,
    }
    
    return render_to_response('dietary.html', variables, context_instance=RequestContext(request))

@login_required
def stipends(request, camptheme):
    camp = get_object_or_404(Camp, theme__iexact=camptheme)
    invitations = Invitation.objects.filter(camp=camp)
    stipends = []
    for invitation in invitations:
        stipendrequests = invitation.stipend_set.all()
        for stipend in stipendrequests:
            stipends.append({
                'user': stipend.invitation.user,
                'first_name': stipend.invitation.user.first_name,
                'last_name': stipend.invitation.user.last_name,
                'url': stipend.invitation.get_absolute_url(),
                'rand_id': stipend.invitation.rand_id,
                'cost_estimate': stipend.cost_estimate,
                'employer_subsidized': stipend.employer_subsidized,
                'employer_percentage': stipend.employer_percentage,
                'invitee_percentage': stipend.invitee_percentage,
                'details': stipend.details,
            })       
    
    variables = {
        'camp': camp,
        'invitations': invitations,
        'stipends': stipends,
    }
    
    return render_to_response('stipends.html', variables, context_instance=RequestContext(request))

@login_required
def sessions(request, camptheme):
    camp = get_object_or_404(Camp, theme__iexact=camptheme)
    invitations = Invitation.objects.filter(camp=camp)
    sessions = []
    for invitation in invitations:
        proposals = invitation.session_set.all()
        for proposal in proposals:
            sessions.append({
                'user': proposal.invitation.user,
                'first_name': proposal.invitation.user.first_name,
                'last_name': proposal.invitation.user.last_name,
                'url': proposal.invitation.get_absolute_url(),
                'rand_id': proposal.invitation.rand_id,
                'title': proposal.title,
                'description': proposal.description,
            })       
    
    variables = {
        'camp': camp,
        'invitations': invitations,
        'sessions': sessions,
    }
    
    return render_to_response('sessions.html', variables, context_instance=RequestContext(request))

def sessions_related(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    camp = invitation.camp    
    invitations = Invitation.objects.filter(camp=camp)
    sessions = []

    for invite in invitations:
        proposals = invite.session_set.all()
        for proposal in proposals:
            sessions.append({
                'user': proposal.invitation.user,
                'first_name': proposal.invitation.user.first_name,
                'last_name': proposal.invitation.user.last_name,
                'title': proposal.title,
                'description': proposal.description,
            })       
    
    variables = {
        'camp': camp,
        'invitation': invitation,
        'invitations': invitations,
        'sessions': sessions,
    }
    
    return render_to_response('sessions_related.html', variables, context_instance=RequestContext(request))
    

@login_required
def google_sync(request, camptheme, deadline=14):
    camp = get_object_or_404(Camp, theme__iexact=camptheme)
    url = camp.spreadsheet_url
    
    myreader = csv.DictReader(urlopen(url))
    today = datetime.date.today()
    rows = []
    
    # Change the number of days in the following line to alter the RSVP response deadline for the new invitations.
    daysleft = timedelta(days=int(deadline))
    expiration_date = today + daysleft
    
    for row in myreader:
        if row['E-mail'] != '' and row['Invite?'] == 'YES':
             combinedname = row['First Name'] + row['Last Name']
             username = slugify(combinedname)
             user, usercreated = User.objects.get_or_create(username=username)
             if usercreated == True:
                 user.email = row['E-mail']
                 user.first_name = row['First Name']
                 user.last_name = row['Last Name']
                 password = User.objects.make_random_password(length=10)
                 user.set_password(password)
                 user.save()
             profile, profilecreated = SparkProfile.objects.get_or_create(user=user)
             if profilecreated == True:
                 profile.email = row['E-mail']
                 profile.employer = row['Organization']
                 if row['POC'] != '0':
                         profile.poc = True
                 if row['W'] != '0':
                         profile.woman = True
                 if row['JOURN?'] != '0':
                         profile.journo = True
                 profile.save()
             invitation, invitecreated = Invitation.objects.get_or_create(user=user,camp=camp)
             if invitecreated == True:
                 invitation.expires = expiration_date
                 invitation.status = 'P'
                 invitation.save()
             rows.append({
                'username': user.username,
                'email': row['E-mail'],
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'employer': row['Organization'],
                'POC': profile.poc,
                'W': profile.woman,
                'J': profile.journo,
                'expires': expiration_date,
                'rand_id': invitation.rand_id,
                })
    
    variables = {
        'rows': rows,
        'camp': camp,
    }
    return render_to_response('google_sync.html', variables, context_instance=RequestContext(request))

@login_required
def mailsync(request, camptheme):
    # Set variables for sync
    ms = MailSnake(settings.MAILCHIMP_API_KEY)
    subscribers = []
    
    # Get relevant Django objects
    camp = get_object_or_404(Camp, theme__iexact=camptheme)
    list_name = camp.mailchimp_list
    invitations = Invitation.objects.filter(camp=camp)
    
    # Adjust Django objects for export
    for invitation in invitations:
        subscribers.append({
            'EMAIL': invitation.user.email,
            'FNAME': invitation.user.first_name,
            'LNAME': invitation.user.last_name,
            'STATUS': invitation.get_status_display(),
            'INVITE': 'http://apps.sparkcamp.com/rsvp/%s' % invitation.rand_id,
            'EXPIRES': invitation.expires.strftime('%B %d, %Y'),
            })
    
    # Get relevant MailSnake objects
    lists = ms.lists()
    
    # MailSnake options
    # No confirmation email to subscribers after adding them to the list
    double_optin = False
    # If members are already found on the list, update their status instead of adding a duplicate subscriber
    update_existing = True
    
    def find_needle(haystack, needle):
        for list in haystack:
                if list['name'] == needle:
                        return list['id']
    
    list_id = find_needle(lists['data'], list_name)
    ms_response = ms.listBatchSubscribe(id=list_id, batch=subscribers, double_optin=double_optin, update_existing=update_existing)
    
    variables = {
        'ms_response': ms_response,
        'camp': camp,
    }
    return render_to_response('mailsync.html', variables, context_instance=RequestContext(request))

def guest_invite(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    # Declare global variables
    today = date.today()
    twoweeks = datetime.timedelta(days=14)
    month = datetime.timedelta(days=30)
    invitation.cancel_by = invitation.camp.start_date - month
    invitation.late_cancellation = invitation.camp.start_date - twoweeks
    update = False
    formvars = False
    detailform = InviteDetailForm()
    sparkprofile = SparkProfile.objects.get(user=invitation.user)
    confirmed = Invitation.objects.filter(camp=invitation.camp).filter(status='Y')
    
    def decideform(formvars={}):
        if invitation.status == 'Y':
            message = '''
            We're looking forward to your attendance at Spark Camp. We happily have you confirmed as coming. Book your hotel and flight soon using the information below.<br /><br />
             
            If for any reason you should have to cancel your attendance, please do so no later than %s, so that we can offer your spot to someone else. We cover the costs of your attendance at Spark Camp, with the support of our generous sponsors. For any cancellations after %s, those costs are unrecoverable, and we'll ask you to repay us a portion of them.
            ''' % (invitation.cancel_by.strftime("%B %e"), invitation.late_cancellation.strftime("%B %e"))
            form = UpdateForm(formvars)
        elif invitation.expires < today:
            message = 'It\'s after the deadline (%s) for your invitation, but ' % (invitation.expires.strftime("%B %e"))
            if invitation.status == 'W':
                message = message + 'we have you on the waitlist, and will update you shortly on whether we can accommodate you. Please let us know if it turns out you can\'t make it after all.'
            else:
                message = message + 'if it turns out you can make it to Spark Camp, we may still be able to accommodate you. If so, please let us know whether we should put you on the waitlist, and we\'ll be in touch very soon with an update.'
            form = WaitlistForm(formvars)
        elif invitation.status == 'N' or invitation.status == 'C':
            message = 'We\'re sorry to hear you can\'t make it to Spark Camp. Please let us know (by %s at the latest) if your plans change in our favor.' % (invitation.cancel_by.strftime("%B %e"))
            form = ResurrectForm(formvars)  
        elif invitation.status == 'W':
            message = 'We have you on the waitlist for Spark Camp, and will update you shortly on whether we can accommodate you. Please let us know if it turns out you can\'t make it.'
            form = WaitlistForm(formvars)
        else:
            message = 'We very much hope you can make it to Spark Camp. Please update your RSVP by %s.' % (invitation.expires.strftime("%B %e"))
            form = ResponseForm(formvars)
        return message, form

    if request.method == 'POST':
        message, form = decideform(request.POST)
        if form.is_valid():
            invitation.status = form.cleaned_data['status']
            invitation.save()
            message, form = decideform(request.POST)
            update = 'Thank you for updating your status.'

            # Send an email confirming their change
            subject = 'Confirming Spark Camp RSVP for %s %s' % (invitation.user.first_name, invitation.user.last_name)
            if invitation.status == 'Y':
                starts = invitation.camp.start_date.strftime("%l:%M %P") + ' on ' + invitation.camp.start_date.strftime("%A, %B %d")
                ends = invitation.camp.end_date.strftime("%l:%M %P") + ' on ' + invitation.camp.end_date.strftime("%A, %B %d")
                url = invitation.get_absolute_url()
                body = '''
This e-mail (happily) confirms your attendance at Spark Camp %s.

Just in case you RSVP'd without reading the full invitation: spaces are only guaranteed to campers who can attend the full camp. It begins at %s, and will end at %s. If you have any questions or concerns, please contact us immediately at team@sparkcamp.com.

As soon as you can, update your bio and contact info, tell us your dietary preferences, and book your flight and hotel. Instructions for doing all of the above are at your personal invitation dashboard: http://apps.sparkcamp.com%s.

Thanks,

Team Spark
                ''' % (invitation.camp.theme, starts, ends, url)
            else: 
                body = message + ' Remember, the URL to update or change your RSVP is http://apps.sparkcamp.com%s.' % invitation.get_absolute_url()
            send_mail(subject, body, 'rsvp@sparkcamp.com', ['rsvp@sparkcamp.com', invitation.user.email], fail_silently=True)
    else:
        message, form = decideform()
        
    # Find roommate requests
    if invitation.roommate_set.all():
        roommates = invitation.roommate_set.all()
        roommate = roommates[0]
        
        # Find potential roommate matches
        roommate.potentials = []
        
        for potential in Roommate.objects.exclude(invitation=invitation):
            if (potential.invitation.camp == invitation.camp):
                if (roommate.roommate == 'A') or (potential.sex == roommate.roommate):
                    if (potential.roommate == 'A') or (roommate.sex == potential.roommate):
                        roommate.potentials.append(potential)
        
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
        ignite.experience = ignite.get_experience_display()
    else:
        ignite = False
    
    # Find session proposals
    if invitation.session_set.all():
        sessions = invitation.session_set.all()
        session = sessions[0]
    else:
        session = False
    
    invitation.pretty_status = invitation.get_status_display()

    variables = {
        'invitation': invitation,
        'sparkprofile': sparkprofile,
        'confirmed': confirmed,
        'form': form,
        'detailform': detailform,
        'update': update,
        'message': message,
        'roommate': roommate,
        'stipend': stipend,
        'ignite': ignite,
        'session': session,
    }

    return render_to_response('single_invite.html', variables, context_instance=RequestContext(request))

def invite_related(request, rand_id, main_object):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    url = invitation.get_absolute_url()
    main_object = eval(main_object)
    try:
        object = main_object.objects.get(invitation=invitation)
    except main_object.DoesNotExist:
        object = main_object(invitation=invitation)
    
    properties = {
        'Roommate': ( 'sex', 'roommate', 'more', ),
        'Ignite': ( 'title', 'experience', 'description', ),
        'Stipend': ( 'cost_estimate', 'employer_subsidized', 'employer_percentage', 'invitee_percentage', 'details', ),
        'Session': ( 'title', 'description', ),
    }
    
    local_dict = properties[main_object.__name__]
    
    if request.method == 'POST':
        form = eval('%sForm(request.POST, instance=object)' % main_object.__name__)
        if form.is_valid():
            for item in local_dict:
                key = compile(item, '', 'exec')
                object.key = form.cleaned_data[item]
            object.save()
            return HttpResponseRedirect(url)
    else:
        form = eval('%sForm(instance=object)' % main_object.__name__)
    
    variables = {
        'invitation': invitation,
        'form': form,
        'object': object,
        'main_object': main_object.__name__,
        'properties': properties,
        'rand_id': rand_id,
    }
    
    return render_to_response('related.html', variables, context_instance=RequestContext(request))

def invite_related_delete(request, rand_id, main_object):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    url = invitation.get_absolute_url()
    main_object = eval(main_object)
    try:
        object = main_object.objects.get(invitation=invitation)
    except main_object.DoesNotExist:
        raise Http404(u'Could not find this %s.' % main_object)
    
    variables = {
        'invitation': invitation,
        'object': object,
        'main_object': main_object.__name__,
        'rand_id': rand_id,
        'url': url,
    }
    
    return render_to_response('related_delete.html', variables, context_instance=RequestContext(request))

def confirm_delete(request, main_object, object_id):
    main_object = eval(main_object)
    object = get_object_or_404(main_object, id=object_id)
    url = object.invitation.get_absolute_url()
    object.delete()
    return HttpResponseRedirect(url)
    
def invite_logistics(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)

    if request.method == 'POST':
        form = InviteDetailForm(request.POST, instance=invitation)
        if form.is_valid():
            invitation.dietary = form.cleaned_data['dietary']
            invitation.arrival_time = form.cleaned_data['arrival_time']
            invitation.departure_time = form.cleaned_data['departure_time']
            invitation.hotel_booked = form.cleaned_data['hotel_booked']
            invitation.save()
            return HttpResponseRedirect('/rsvp/%s/' % invitation.rand_id)
    else:
        form = InviteDetailForm(instance=invitation)
    
    variables = {
        'invitation': invitation,
        'form': form,
    }
    
    return render_to_response('logistics.html', variables, context_instance=RequestContext(request))
    
def profile(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    user = invitation.user
    profile = SparkProfile.objects.get(user=user)
    
    if request.method == 'POST':
        form = SparkProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile.bio = form.cleaned_data['bio']
            profile.job_title = form.cleaned_data['job_title']
            profile.employer = form.cleaned_data['employer']
            profile.url = form.cleaned_data['url']
            profile.twitter = form.cleaned_data['twitter']
            profile.phone = form.cleaned_data['phone']
            profile.email = form.cleaned_data['email']
            profile.dietary = form.cleaned_data['dietary']
            user.email = form.cleaned_data['email']
            profile.save()
            user.save()
            return HttpResponseRedirect('/rsvp/%s' % invitation.rand_id)
    else:
        form = SparkProfileForm(instance=profile)
    
    variables = {
        'invitation': invitation,
        'profile': profile,
        'form': form,
    }
    
    return render_to_response('profile.html', variables, context_instance=RequestContext(request))
