# coding: utf-8

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import Context, RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render_to_response, redirect
from rsvp.models import *
from rsvp.forms import *
from rsvp.mailsnake import MailSnake
import random, csv, datetime, unicodecsv
from datetime import date, timedelta
from urllib import urlopen

##########
# Admin views
##########

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
    invitee_pocs = invitations.filter(user__sparkprofile__poc=True)
    invitee_women = invitations.filter(user__sparkprofile__woman=True)
    invitee_journos = invitations.filter(user__sparkprofile__journo=True)
    
    def percent(part, whole):
        denominator = float(len(whole))
        numerator = float(len(part))
        if denominator <= 0:
            denominator = 1
        return int(100 * (numerator/denominator))
        
    percent_poc = percent(confirmed_pocs, confirmed)
    percent_women = percent(confirmed_women, confirmed)
    percent_journos = percent(confirmed_journos, confirmed)
    percent_all_poc = percent(invitee_pocs, invitations)
    percent_all_women = percent(invitee_women, invitations)
    percent_all_journos = percent(invitee_journos, invitations)
    
    variables = {
        'camp': camp,
        'invitations': invitations,
        'confirmed': confirmed,
        'percent_poc': percent_poc,
        'percent_women': percent_women,
        'percent_journos': percent_journos,
        'percent_all_poc': percent_all_poc,
        'percent_all_women': percent_all_women,
        'percent_all_journos': percent_all_journos,
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
            if usercreated == True:
                profile.email = row['E-mail']
            profile.employer = row['Organization']
            if row['POC'] == '1':
                profile.poc = True
            if row['W'] == '1':
                profile.woman = True
            if row['Journ?'] == '1':
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
        profile = SparkProfile.objects.get(user=invitation.user)
        subscribers.append({
            'EMAIL': invitation.user.email,
            'EMAIL2': profile.secondary_email,
            'FNAME': invitation.user.first_name,
            'LNAME': invitation.user.last_name,
            'STATUS': invitation.get_status_display(),
            'INVITE': 'https://imp.sparkcamp.com/register/%s' % invitation.rand_id,
            'EXPIRES': invitation.expires.strftime('%B %e, %Y'),
            'BIO': profile.bio,
            'TWITTER': profile.twitter,
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

















##########
# Admin views - REBOOTED TEMPLATE
##########

@login_required
def dashboard(request):
    today = date.today()
    upcoming = Camp.objects.filter(start_date__gte=today)
    past = Camp.objects.filter(start_date__lte=today)
    
    variables = {
        'upcoming' : upcoming,
        'past': past,
    }
    return render_to_response('reboot/reboot.html', variables, context_instance=RequestContext(request))

@login_required
def camp(request, camptheme):
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
    invitee_pocs = invitations.filter(user__sparkprofile__poc=True)
    invitee_women = invitations.filter(user__sparkprofile__woman=True)
    invitee_journos = invitations.filter(user__sparkprofile__journo=True)
    
    def percent(part, whole):
        denominator = float(len(whole))
        numerator = float(len(part))
        if denominator <= 0:
            denominator = 1
        return int(100 * (numerator/denominator))
        
    percent_poc = percent(confirmed_pocs, confirmed)
    percent_women = percent(confirmed_women, confirmed)
    percent_journos = percent(confirmed_journos, confirmed)
    percent_all_poc = percent(invitee_pocs, invitations)
    percent_all_women = percent(invitee_women, invitations)
    percent_all_journos = percent(invitee_journos, invitations)
    
    variables = {
        'camp': camp,
        'invitations': invitations,
        'confirmed': confirmed,
        'percent_poc': percent_poc,
        'percent_women': percent_women,
        'percent_journos': percent_journos,
        'percent_all_poc': percent_all_poc,
        'percent_all_women': percent_all_women,
        'percent_all_journos': percent_all_journos,
    }
    return render_to_response('reboot/camp.html', variables, context_instance=RequestContext(request))


  
  
  




##########
# Registration views - REBOOTED TEMPLATE
##########

def route(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    if invitation.status == 'I':
        return redirect('update', rand_id=rand_id)
    if invitation.status == 'N' or invitation.status == 'C':
        return redirect('restore', rand_id=rand_id)
    if invitation.status == 'Y':
        return redirect('details', rand_id=rand_id)
    if invitation.status == 'W':
        return redirect('waitlist', rand_id=rand_id)
    else:
        return redirect('invite', rand_id=rand_id)

def invite(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)

    if invitation.status == 'N' or invitation.status == 'C':
        return redirect('route', rand_id=rand_id)
    
    if invitation.camp.paid:
        import stripe
        from invites2.settings import STRIPE_PUBLIC_KEY
        invitation.key = STRIPE_PUBLIC_KEY
        invitation.stripe_cost = invitation.price() * 100
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
    }
    return render_to_response('reboot/invite.html', variables, context_instance=RequestContext(request))
  
def pay(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    profile = invitation.user.sparkprofile
    profileform = SparkProfileForm(instance=profile)
    
    # If the user has submitted a form
    if request.method == 'POST':
        # If the invitation isn't a comp ticket
        if invitation.comp_ticket != True:
            import stripe
            from invites2.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
            stripe.api_key = STRIPE_SECRET_KEY    
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            error = False

            invitation.cost = invitation.price()
            invitation.stripe_cost = invitation.price() * 100;
            invitation.key = STRIPE_PUBLIC_KEY

            # Create the charge on Stripe's servers - this will charge the user's card
            try:
                charge = stripe.Charge.create(
                  amount=invitation.stripe_cost, # amount in cents, again
                  currency="usd",
                  card=token,
                  description=invitation.user.username
                )
            except stripe.CardError, e:
            # The card has been declined
                body = e.json_body
                error  = body['error']
                pass

            if error:
                invitation.has_paid = False
            else:
                invitation.has_paid = True
        # If this is actually a comp ticket, just process it as paid
        else:
            invitation.has_paid = True
            if (invitation.has_paid == True) and (invitation.user.sparkprofile.bio != '') and (invitation.user.sparkprofile.has_headshot == True):
                invitation.status = 'Y'
            else:
                invitation.status = 'I'
        
        invitation.save()
        
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
        'cost': invitation.cost,
        'token': token,
        'email': email,
        'error': error,
        'profileform': profileform,
    }
    return render_to_response('reboot/pay.html', variables, context_instance=RequestContext(request))

def update(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    user = invitation.user
    profile = SparkProfile.objects.get(user=user)
    
    # Redirect users who've said they can't attend to put them on the waitlist.
    if invitation.status == 'N' or invitation.status == 'C':
        return redirect('restore', rand_id=rand_id)    

    # If the user has submitted a profile form ...
    if request.method == 'POST':
        profileform = SparkProfileForm(request.POST, instance=profile)

        # ... and that form is valid ...
        if profileform.is_valid():
            profile.bio = profileform.cleaned_data['bio']
            profile.job_title = profileform.cleaned_data['job_title']
            profile.employer = profileform.cleaned_data['employer']
            profile.url = profileform.cleaned_data['url']
            profile.twitter = profileform.cleaned_data['twitter']
            profile.phone = profileform.cleaned_data['phone']
            profile.email = profileform.cleaned_data['email']
            profile.dietary = profileform.cleaned_data['dietary']
            profile.has_headshot = profileform.cleaned_data['has_headshot']
            user.email = profileform.cleaned_data['email']
            profile.save()
            user.save()

            # ... AND that form has a bio and headshot ...
            if profile.bio != '' and profile.has_headshot == True:

                # If the user is on the waitlist, merely update their information. Send no email.
                if invitation.status == 'W':
                    messages.success(request, 'Thank you for updating your information! We\'ll let you know as soon as possible if we can accommodate you at %s' % (invitation.camp.display_name))
                    return redirect('waitlist', rand_id=rand_id)
                
                # And if they're not on the waitlist, then ...
                else: 
                    
                    # If they're already confirmed, also just update; no email.
                    if invitation.status == 'Y':
                        messages.success(request, '%s, thank you for updating your information!' % (user.first_name))
                    
                    # Otherwise, set them as confirmed, and send a confirmation email.
                    else:
                        messages.success(request, '%s, you\'re now registered for %s.' % (user.first_name, invitation.camp.display_name))
                        invitation.status = 'Y'
                        
                        # Confirmation email
                        date_format = '%A, %B %d, %Y'
                        confirmdict = {
                            'first_name': user.first_name,
                            'last_name': user.first_name,
                            'display_name': invitation.camp.display_name,
                            'description': invitation.camp.description,
                            'logistics': invitation.camp.logistics,
                            'cancel_by': invitation.camp.cancel_by.strftime(date_format),
                            'venue': invitation.camp.venue,
                            'venue_address': invitation.camp.venue_address,
                            'hotel': invitation.camp.hotel,
                            'hotel_link': invitation.camp.hotel_link,
                            'hotel_code': invitation.camp.hotel_code,
                            'invite_link': settings.EXTERNAL_URL + invitation.get_absolute_url(),
                        }
                        body = invitation.camp.confirmation_email % confirmdict
                        subject = 'Confirming your registration for %s' % invitation.camp.display_name
                        if settings.DEBUG == False:
                            email = user.email
                        else:
                            email = settings.EMAIL_TEST
                        send_mail(subject, body, 'rsvp@sparkcamp.com', ['rsvp@sparkcamp.com', email], fail_silently=True)
                        
                    invitation.save()
                    return redirect('details', rand_id=rand_id)
            else:
                invitation.status = 'I'
                messages.warning(request, 'We\'re still missing some key pieces of info to finalize your registration.')
                invitation.save()
                
    else:
        profileform = SparkProfileForm(instance=profile)
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
        'profile': profile,
        'profileform': profileform,
    }
    return render_to_response('reboot/update.html', variables, context_instance=RequestContext(request))
  
def details(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    invitation.pretty_status = invitation.get_status_display()
    confirmed = Invitation.objects.filter(camp=invitation.camp).filter(status='Y').order_by('user__last_name')

    if invitation.status != 'Y':
        return redirect('route', rand_id=rand_id)
    
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
        'camp': invitation.camp,
        'confirmed': confirmed,
        'roommate': roommate,
        'stipend': stipend,
        'ignite': ignite,
        'session': session,
    }
    return render_to_response('reboot/details.html', variables, context_instance=RequestContext(request))

def stipend(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    url = invitation.get_absolute_url()
    stipend, created = Stipend.objects.get_or_create(invitation=invitation)

    if request.method == 'POST':
        form = StipendForm(request.POST, instance=stipend)
        if form.is_valid():
            stipend.cost_estimate = form.cleaned_data['cost_estimate']
            stipend.employer_subsidized = form.cleaned_data['employer_subsidized']
            stipend.employer_percentage = form.cleaned_data['employer_percentage']
            stipend.invitee_percentage = form.cleaned_data['invitee_percentage']
            stipend.details = form.cleaned_data['details']
            stipend.save()
            invitation.has_paid = True
            if invitation.user.sparkprofile.bio != '' and invitation.user.sparkprofile.has_headshot == True:
                invitation.status = 'Y'
            else:
                invitation.status = 'I'
            invitation.user.save()
            invitation.save()
            return redirect('route', rand_id=rand_id)
    else:
        form = StipendForm(instance=stipend)
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
        'form': form,
        'stipend': stipend,
    }
    
    return render_to_response('reboot/stipend.html', variables, context_instance=RequestContext(request))

def cancel(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    today = datetime.date.today()
    cancel_by = invitation.camp.cancel_by.date()
    
    if today > cancel_by:
        invitation.partial_refund = True
    else:
        invitation.partial_refund = False
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
    }
    return render_to_response('reboot/cancel.html', variables, context_instance=RequestContext(request))

def confirm_cancel(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    messages.warning(request, 'Your registration has been canceled. Again, we\'re sad to hear you can\'t make it. If your circumstances change, please do let us know.')
    
    invitation.status = 'C'
    invitation.save()
    
    return redirect('restore', rand_id=rand_id)

def restore(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
    }
    return render_to_response('reboot/restore.html', variables, context_instance=RequestContext(request))

def confirm_restore(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    invitation.status = 'W'
    invitation.save()
    messages.success(request, 'Thanks for letting us know you can make it! We have you on the waitlist, and we\'ll let you know as soon as possible whether we can still accommodate you.')
    return redirect('route', rand_id=rand_id)

def waitlist(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)

    if invitation.status != 'W':
        return redirect('route', rand_id=rand_id)
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
    }
    return render_to_response('reboot/waitlist.html', variables, context_instance=RequestContext(request))

def signup(request, rand_id, main_object):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    main_object = eval(main_object)
    try:
        object = main_object.objects.get(invitation=invitation)
    except main_object.DoesNotExist:
        object = main_object(invitation=invitation)
    
    properties = {
        'Roommate': ( 'sex', 'roommate', 'more', ),
        'Ignite': ( 'title', 'experience', 'description', ),
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
            messages.success(request, 'You\'ve got it. You\'re on the %s List.' % (main_object.__name__))
            return redirect('route', rand_id=rand_id)
    else:
        form = eval('%sForm(instance=object)' % main_object.__name__)
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
        'form': form,
        'object': object,
        'main_object': main_object.__name__,
        'properties': properties,
        'rand_id': rand_id,
    }
    
    return render_to_response('reboot/signup.html', variables, context_instance=RequestContext(request))

def signdown(request, rand_id, main_object):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    main_object = eval(main_object)
    try:
        object = main_object.objects.get(invitation=invitation)
    except main_object.DoesNotExist:
        raise Http404(u'Could not find this %s.' % main_object)
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
        'object': object,
        'main_object': main_object.__name__,
        'rand_id': rand_id,
    }
    
    return render_to_response('reboot/signdown.html', variables, context_instance=RequestContext(request))
  
def delete_signup(request, main_object, object_id, rand_id):
  main_object = eval(main_object)
  object = get_object_or_404(main_object, id=object_id)
  object.delete()
  messages.success(request, 'You\'ve got it. You\'re no longer on the %s List.' % (main_object.__name__))
  return redirect('route', rand_id=rand_id)


##########
# Registration views - UPSTATEMENT TEMPLATE
##########

def route_registration(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    if invitation.status == 'P' or invitation.status == 'Q':
        return redirect('register', rand_id=rand_id)
    if invitation.status == 'I':
        return redirect('registration_complete', rand_id=rand_id)
    if invitation.status == 'N' or invitation.status == 'C':
        return redirect('registration_restore', rand_id=rand_id)
    if invitation.status == 'Y':
        return redirect('registered', rand_id=rand_id)
    else:
        return redirect('register', rand_id=rand_id)
      
def register(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    if invitation.status == 'I' or invitation.status == 'Y':
        return redirect('registration_complete', rand_id=rand_id)
    
    if invitation.camp.paid:
        import stripe
        from invites2.settings import STRIPE_PUBLIC_KEY
        invitation.key = STRIPE_PUBLIC_KEY
        invitation.cost = invitation.price() * 100
    
    variables = {
        'invitation': invitation,
    }
    return render_to_response('register.html', variables, context_instance=RequestContext(request))

def receive_payment(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    profile = invitation.user.sparkprofile
    profileform = SparkProfileForm(instance=profile)

    if request.method == 'POST':
        import stripe
        from invites2.settings import STRIPE_SECRET_KEY
        stripe.api_key = STRIPE_SECRET_KEY    
        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        error = False

        invitation.cost = invitation.price()
        
        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
              amount=invitation.cost * 100, # amount in cents, again
              currency="usd",
              card=token,
              description=invitation.user.username
            )
        except stripe.CardError, e:
        # The card has been declined
            body = e.json_body
            error  = body['error']
            pass
        
        if error:
            invitation.has_paid = False
        else:
            invitation.has_paid = True
            if (invitation.has_paid == True) and (invitation.user.sparkprofile.bio != '') and (invitation.user.sparkprofile.has_headshot == True):
                invitation.status = 'Y'
            else:
                invitation.status = 'I'
        
        invitation.save()
        
    variables = {
        'invitation': invitation,
        'cost': invitation.cost,
        'token': token,
        'email': email,
        'error': error,
        'profileform': profileform,
    }
    return render_to_response('receive_payment.html', variables, context_instance=RequestContext(request))

def registration_complete(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    user = invitation.user
    profile = SparkProfile.objects.get(user=user)
    
    if request.method == 'POST':
        profileform = SparkProfileForm(request.POST, instance=profile)
        if profileform.is_valid():
            profile.bio = profileform.cleaned_data['bio']
            profile.job_title = profileform.cleaned_data['job_title']
            profile.employer = profileform.cleaned_data['employer']
            profile.url = profileform.cleaned_data['url']
            profile.twitter = profileform.cleaned_data['twitter']
            profile.phone = profileform.cleaned_data['phone']
            profile.email = profileform.cleaned_data['email']
            profile.dietary = profileform.cleaned_data['dietary']
            profile.has_headshot = profileform.cleaned_data['has_headshot']
            user.email = profileform.cleaned_data['email']
            if profile.bio != '' and profile.has_headshot == True:
                invitation.status = 'Y'
                profile.save()
                user.save()
                invitation.save()
                confirmation_message = '''
                %s, your %s registration is now complete! You will soon receive a confirmation email from us, which includes travel and hotel recommendations.
                ''' % (user.first_name, invitation.camp.display_name)
                variables = {
                    'invitation': invitation,
                    'confirmation_message': confirmation_message,
                }
                return render_to_response('registered.html', variables, context_instance=RequestContext(request))
            else:
                invitation.status = 'I'
                profile.save()
                user.save()
                invitation.save()
                
    else:
        profileform = SparkProfileForm(instance=profile)
    
    variables = {
        'invitation': invitation,
        'profile': profile,
        'profileform': profileform,
    }
    return render_to_response('registration_complete.html', variables, context_instance=RequestContext(request))

def registration_update(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    user = invitation.user
    profile = SparkProfile.objects.get(user=user)
    update = True
    
    if request.method == 'POST':
        profileform = SparkProfileForm(request.POST, instance=profile)
        if profileform.is_valid():
            profile.bio = profileform.cleaned_data['bio']
            profile.job_title = profileform.cleaned_data['job_title']
            profile.employer = profileform.cleaned_data['employer']
            profile.url = profileform.cleaned_data['url']
            profile.twitter = profileform.cleaned_data['twitter']
            profile.phone = profileform.cleaned_data['phone']
            profile.email = profileform.cleaned_data['email']
            profile.dietary = profileform.cleaned_data['dietary']
            profile.has_headshot = profileform.cleaned_data['has_headshot']
            user.email = profileform.cleaned_data['email']
            invitation.status = 'Y'
            profile.save()
            user.save()
            invitation.save()
            return redirect('registered', rand_id=invitation.rand_id)
    else:
        profileform = SparkProfileForm(instance=profile)
    
    variables = {
        'invitation': invitation,
        'profile': profile,
        'profileform': profileform,
        'update': update,
    }
    return render_to_response('registration_complete.html', variables, context_instance=RequestContext(request))

def registered(request, rand_id, confirmation_message=False):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    invitation.pretty_status = invitation.get_status_display()
    user = invitation.user
    profile = invitation.user.sparkprofile
    confirmed = Invitation.objects.filter(camp=invitation.camp).filter(status='Y').order_by('user__last_name')
    
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
        'confirmed': confirmed,
        'roommate': roommate,
        'stipend': stipend,
        'ignite': ignite,
        'session': session,
        'confirmation_message': confirmation_message,
        'profile': profile,
        'user': user,
    }
    return render_to_response('registered.html', variables, context_instance=RequestContext(request))

def registration_cancel(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    today = datetime.date.today()
    cancel_by = invitation.camp.cancel_by.date()
    
    if today > cancel_by:
        invitation.partial_refund = True
    else:
        invitation.partial_refund = False
    
    variables = {
        'invitation': invitation,
        'camp': invitation.camp,
    }
    return render_to_response('reboot/cancel.html', variables, context_instance=RequestContext(request))

def registration_confirm_cancel(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    invitation.status = 'C'
    invitation.save()
    
    return redirect('registration_restore', rand_id=rand_id)

def registration_restore(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    variables = {
        'invitation': invitation,
    }
    return render_to_response('registration_restore.html', variables, context_instance=RequestContext(request))

def register_stipend(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    url = invitation.get_absolute_url()
    stipend, created = Stipend.objects.get_or_create(invitation=invitation)

    if request.method == 'POST':
        form = StipendForm(request.POST, instance=stipend)
        if form.is_valid():
            stipend.cost_estimate = form.cleaned_data['cost_estimate']
            stipend.employer_subsidized = form.cleaned_data['employer_subsidized']
            stipend.employer_percentage = form.cleaned_data['employer_percentage']
            stipend.invitee_percentage = form.cleaned_data['invitee_percentage']
            stipend.details = form.cleaned_data['details']
            stipend.save()
            invitation.status = 'I'
            invitation.user.save()
            invitation.save()
            return HttpResponseRedirect('/register/%s' % invitation.rand_id)
    else:
        form = StipendForm(instance=stipend)
    
    variables = {
        'invitation': invitation,
        'form': form,
        'stipend': stipend,
    }
    
    return render_to_response('register_stipend.html', variables, context_instance=RequestContext(request))

def register_related(request, rand_id, main_object):
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
    
    return render_to_response('register_related.html', variables, context_instance=RequestContext(request))

def register_related_delete(request, rand_id, main_object):
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
    
    return render_to_response('register_related_delete.html', variables, context_instance=RequestContext(request))

def register_confirm_delete(request, main_object, object_id):
    main_object = eval(main_object)
    object = get_object_or_404(main_object, id=object_id)
    url = object.invitation.get_absolute_url()
    object.delete()
    return HttpResponseRedirect(url)

##########
# Deprecated invitation views
##########

def guest_invite(request, rand_id):
    invitation = get_object_or_404(Invitation, rand_id=rand_id)
    
    # Declare global variables
    today = date.today()
    twoweeks = datetime.timedelta(days=14)
    month = datetime.timedelta(days=30)
    # invitation.cancel_by = invitation.camp.start_date - month
    # invitation.late_cancellation = invitation.camp.start_date - twoweeks
    update = False
    formvars = False
    detailform = InviteDetailForm()
    sparkprofile = SparkProfile.objects.get(user=invitation.user)
    confirmed = Invitation.objects.filter(camp=invitation.camp).filter(status='Y').order_by('user__last_name')
    
    def decideform(formvars={}):
        if invitation.status == 'Y':
            message = '''
            We're looking forward to your attendance. We happily have you confirmed as coming. Book your hotel and flight soon using the information below.<br /><br />
             
            If for any reason you should have to cancel your attendance, please do so no later than %s, so that we can offer your spot to someone else. We cover the costs of your attendance at this event, with the support of our generous sponsors. For any cancellations after %s, those costs are unrecoverable, and we'll ask you to repay us a portion of them.
            ''' % (invitation.expires.strftime("%B %e"), invitation.expires.strftime("%B %e"))
            form = UpdateForm(formvars)
        elif invitation.expires < today:
            message = 'It\'s after the deadline (%s) for your invitation, but ' % (invitation.expires.strftime("%B %e"))
            if invitation.status == 'W':
                message = message + 'we have you on the waitlist, and will update you shortly on whether we can accommodate you. Please let us know if it turns out you can\'t make it after all.'
            else:
                message = message + 'if it turns out you can make it to the event, we may still be able to accommodate you. If so, please let us know whether we should put you on the waitlist, and we\'ll be in touch very soon with an update.'
            form = WaitlistForm(formvars)
        elif invitation.status == 'N' or invitation.status == 'C':
            message = 'We\'re sorry to hear you can\'t make it to the event. Please let us know (by %s at the latest) if your plans change in our favor.' % (invitation.cancel_by.strftime("%B %e"))
            form = ResurrectForm(formvars)  
        elif invitation.status == 'W':
            message = 'We have you on the waitlist for the event, and will update you shortly on whether we can accommodate you. Please let us know if it turns out you can\'t make it.'
            form = WaitlistForm(formvars)
        else:
            message = 'We very much hope you can make it to the event. Please update your RSVP by %s.' % (invitation.expires.strftime("%B %e"))
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
            subject = 'Confirming RSVP for %s %s' % (invitation.user.first_name, invitation.user.last_name)
            if invitation.status == 'Y':
                starts = invitation.camp.start_date.strftime("%l:%M %P") + ' on ' + invitation.camp.start_date.strftime("%A, %B %d")
                ends = invitation.camp.end_date.strftime("%l:%M %P") + ' on ' + invitation.camp.end_date.strftime("%A, %B %d")
                url = invitation.get_absolute_url()
                body = '''
This e-mail (happily) confirms your attendance at Spark %s.

Just in case you RSVP'd without reading the full invitation: spaces are only guaranteed to attendees who can attend the full weekend. It begins at %s, and will end at %s. If you have any questions or concerns, please contact us immediately at team@sparkcamp.com.

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

@login_required
def camp_table(request, camptheme):
    camp = get_object_or_404(Camp, theme__iexact=camptheme)
    invitations = Invitation.objects.filter(camp=camp)
    confirmed = invitations.filter(status='Y')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_invitees_for_' + camp.short_name + '.csv"'
    writer = unicodecsv.writer(response)    

    writer.writerow(['Username', 'First name', 'Last name', 'Email address', 'Email 2', 'Phone', 'Job title', 'Organization', 'Bio', 'Twitter', 'URL', 'W', 'POC', 'J', 'Dietary needs', 'Headshot sent', 'Expires', 'Custom message', 'Invitation status', 'Special cost', 'Stipend requested', 'Has paid', 'Comp ticket'])
    
    for invite in invitations:
        profile = SparkProfile.objects.get(user=invite.user)
        if invite.stipend_set.all():
            stipend = True
        else:
            stipend = False
            
        writer.writerow([invite.user.username, invite.user.first_name, invite.user.last_name, invite.user.email, profile.secondary_email, profile.phone, profile.job_title, profile.employer, profile.bio, profile.twitter, profile.url, profile.woman, profile.poc, profile.journo, profile.dietary, profile.has_headshot, invite.expires, invite.custom_message, invite.status, invite.special_cost, stipend, invite.has_paid, invite.comp_ticket])
        
    return response

@login_required
def user_table(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_campers.csv"'
    writer = unicodecsv.writer(response)
    users = User.objects.all()
    
    writer.writerow(['Username', 'First name', 'Last name', 'Email address', 'Job title', 'Organization', 'Camps attended', 'Camps invited to', 'Camps nominated for'])
    
    for user in users:
        invitations = Invitation.objects.filter(user=user)
        profile = SparkProfile.objects.get(user=user)
        writer.writerow([user.username, user.first_name, user.last_name, user.email, profile.job_title, profile.employer, '', '', ''])
        
    return response