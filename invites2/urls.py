from django.conf.urls import patterns, include, url, static
from django.contrib.auth.views import login, logout_then_login
from rsvp.views import *
from nod.views import search

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'invites2.views.home', name='home'),
    # url(r'^invites2/', include('invites2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^$', dashboard, name="dashboard"),
    url(r'^camp/(?P<camptheme>[a-zA-Z-,& ]+)/$', camp, name="camp"),
    url(r'^camp/(?P<camptheme>[a-zA-Z-,& ]+)/csv/$', camp_table, name="camp_table"),
    url(r'^camps/$', camps, name="camps"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/dietary/$', dietary, name="dietary"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/stipends/$', stipends, name="stipends"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/sessions/$', sessions, name="sessions"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/gsync/$', google_sync, name="google_sync"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/gsync/(?P<deadline>\d{1,3})$', google_sync, name="google_sync"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/mailsync/$', mailsync, name="mailsync"),
    url(r'^user/(\w+)/$', user_page, name="user_page"),
    url(r'^usercsv/$', user_table, name="user_table"),
    url(r'^route/(?P<rand_id>\d{8})/$', route, name="route"),
    url(r'^rsvp/(?P<rand_id>\d{8})/$', invite, name="invite"),
    url(r'^rsvp/(?P<rand_id>\d{8})/pay/$', pay, name="pay"),
    url(r'^rsvp/(?P<rand_id>\d{8})/update/$', update, name="update"),
    url(r'^rsvp/(?P<rand_id>\d{8})/details/$', details, name="details"),
    url(r'^rsvp/(?P<rand_id>\d{8})/stipend/$', stipend, name="stipend"),
    url(r'^rsvp/(?P<rand_id>\d{8})/cancel/$', cancel, name="cancel"),
    url(r'^rsvp/(?P<rand_id>\d{8})/confirm_cancel/$', confirm_cancel, name="confirm_cancel"),
    url(r'^rsvp/(?P<rand_id>\d{8})/restore/$', restore, name="restore"),
    url(r'^rsvp/(?P<rand_id>\d{8})/confirm_restore/$', confirm_restore, name="confirm_restore"),
    url(r'^rsvp/(?P<rand_id>\d{8})/waitlist/$', waitlist, name="waitlist"),
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/signup/$', signup, name="signup"),
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/signdown/$', signdown, name="signdown"),
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/(?P<object_id>\d+)/delete/$', delete_signup, name="delete_signup"),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout_then_login),
    url(r'^search/$', search, name="search"),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
