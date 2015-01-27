from django.conf.urls import patterns, include, url, static
from django.contrib.auth.views import login, logout_then_login
from rsvp.views import *
from nod.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'invites2.views.home', name='home'),
    # url(r'^invites2/', include('invites2.foo.urls')),

    url(r'^$', dashboard, name="dashboard"), # lists upcoming and recent camps
    url(r'^camp/(?P<camptheme>[a-zA-Z-,& ]+)/$', camp, name="camp"), # camp dashboard
    url(r'^camp/(?P<camptheme>[a-zA-Z-,& ]+)/contacts/$', contacts, name="contacts"), # one-on-one contacts
    url(r'^camp/(?P<camptheme>[a-zA-Z-,& ]+)/mailchimp/setup/$', mailcamp, name="mailcamp"), # setup camp in MailChimp
    url(r'^camp/(?P<camptheme>[a-zA-Z-,& ]+)/mailchimp/sync/$', mailsync, name="mailsync"), # sync invites with MailChimp
    url(r'^camp/(?P<camptheme>[a-zA-Z-,& ]+)/csv/$', camp_table, name="camp_table"), # CSV of all camp invitees
    url(r'^usercsv/$', user_table, name="user_table"), # CSV of all users
    url(r'^route/(?P<rand_id>\d{8})/$', route, name="route"), # routes incoming users based on invitation status
    url(r'^route/(?P<rand_id>\d{8})/faq/$', faq, name="faq"), #faq
    url(r'^rsvp/(?P<rand_id>\d{8})/$', invite, name="invite"), # first landing page for invitees
    url(r'^rsvp/(?P<rand_id>\d{8})/pay/$', pay, name="pay"), # processes payment for camp registration
    url(r'^rsvp/(?P<rand_id>\d{8})/update/$', update, name="update"), # allows invitees to update profile information and complete registration
    url(r'^rsvp/(?P<rand_id>\d{8})/details/$', details, name="details"), # landing page for confirmed attendees
    url(r'^rsvp/(?P<rand_id>\d{8})/stipend/$', stipend, name="stipend"), # stipend request form
    url(r'^rsvp/(?P<rand_id>\d{8})/cancel/$', cancel, name="cancel"), # registration cancellation page
    url(r'^rsvp/(?P<rand_id>\d{8})/confirm_cancel/$', confirm_cancel, name="confirm_cancel"), # registration cancellation confirmation
    url(r'^rsvp/(?P<rand_id>\d{8})/restore/$', restore, name="restore"), # allows users who've canceled or refused to request waitlisting
    url(r'^rsvp/(?P<rand_id>\d{8})/confirm_restore/$', confirm_restore, name="confirm_restore"), # waitlist request confirm
    url(r'^rsvp/(?P<rand_id>\d{8})/waitlist/$', waitlist, name="waitlist"), # landing page for waitlisted users
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/signup/$', signup, name="signup"), # allows users to sign up for roommates, ignite talks, etc.
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/signdown/$', signdown, name="signdown"), # allows users to cancel roommate/ignite/etc signups
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/(?P<object_id>\d+)/delete/$', delete_signup, name="delete_signup"), # confirmation of cancellation

    # Nod views
    url(r'^search/$', search, name="search"), # generic search of all users
    url(r'^search/nominate/$', search, {'nominate': True}, name="nodsearch"), # search for potential nominees for camp
    # url(r'^(?P<camptheme>[a-zA-Z-,& ]+)/nominate/$', search, {'nominate': True}, name="nodsearch"), # nominate users for a particular camp
    url(r'^nominated/$', nominated, name="nominated"), # nominated users
    url(r'^vote/(?P<round>\d+)/$', vote, name="vote"), # voting table
    url(r'^round/(?P<round>\d+)/$', round, name="round"), # voting round breakdown
    url(r'^invites/(?P<camptheme>[a-zA-Z-,& ]+)/$', invites, name="invites"), # post-vote invite
    url(r'^process/$', process_emails, name="process_emails"), # voting round breakdown


    # Deprecated views (replace these!)
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/dietary/$', dietary, name="dietary"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/stipends/$', stipends, name="stipends"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/sessions/$', sessions, name="sessions"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/mailsync/$', mailsync, name="mailsync"),
    url(r'^user/(\w+)/$', user_page, name="user_page"),
                       
    # Third-party views
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
                       
    # Django.contrib views                   
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout_then_login),
    
    # For flatpages to work, this apparently has to come last
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
