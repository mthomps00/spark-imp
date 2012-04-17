from django.conf.urls import patterns, include, url
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
    url(r'^camps/([a-zA-Z-]+)/$', single_camp, name="single_camp"),
    url(r'^user/(\w+)/$', user_page, name="user_page"),
    url(r'^rsvp/(\d{8})/$', guest_invite, name="invitation"),
    url(r'^rsvp/(\d{8})/logistics/$', invite_logistics, name="invite_logistics"),
    url(r'^rsvp/(\d{8})/profile/$', profile, name="profile"),
    url(r'^rsvp/(?P<rand_id>\d{8})/(?P<main_object>\w+)/$', invite_related, name="invite_related"),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout_then_login),
)
