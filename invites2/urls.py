from django.conf.urls import patterns, include, url, static
from django.contrib.auth.views import login, logout_then_login
from rsvp.views import *

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
    url(r'^$', main_page, name="main_page"),
    url(r'^camps/$', camps, name="camps"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/$', single_camp, name="single_camp"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/dietary/$', dietary, name="dietary"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/stipends/$', stipends, name="stipends"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/sessions/$', sessions, name="sessions"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/gsync/$', google_sync, name="google_sync"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/gsync/(?P<deadline>\d{1,3})$', google_sync, name="google_sync"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/mailsync/$', mailsync, name="mailsync"),
    url(r'^camps/(?P<camptheme>[a-zA-Z-,& ]+)/table/$', camp_table, name="camp_table"),
    url(r'^user/(\w+)/$', user_page, name="user_page"),
    url(r'^usercsv/$', user_table, name="user_table"),
    url(r'^rsvp/(\d{8})/$', guest_invite, name="invitation"),
    url(r'^rsvp/(\d{8})/logistics/$', invite_logistics, name="invite_logistics"),
    url(r'^rsvp/(\d{8})/profile/$', profile, name="profile"),
    url(r'^rsvp/(?P<rand_id>\d{8})/sessions/$', sessions_related, name="sessions_related"),
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/$', invite_related, name="invite_related"),
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/delete/$', invite_related_delete, name="invite_related_delete"),
    url(r'^register/(?P<rand_id>\d{8})/$', route_registration, name="route_registration"),
    url(r'^register/(?P<rand_id>\d{8})/attend/$', register, name="register"),
    url(r'^register/(?P<rand_id>\d{8})/confirm/$', registration_confirm, name="registration_confirm"),
    url(r'^register/(?P<rand_id>\d{8})/update/$', registration_update, name="registration_update"),
    url(r'^register/(?P<rand_id>\d{8})/pay/$', receive_payment, name="receive_payment"),
    url(r'^(?P<main_object>\w+)/(?P<object_id>\d+)/confirmdelete/$', confirm_delete, name="confirm_delete"),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout_then_login),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)
