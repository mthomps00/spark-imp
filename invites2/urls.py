from django.conf.urls import patterns, include, url
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
    (r'^$', main_page),
    (r'^camps/$', camps),
    (r'^camps/([a-zA-Z-]+)/$', single_camp),
    (r'^user/(\w+)/$', user_page),
    (r'^rsvp/(\d+)/$', guest_invite),
    (r'^rsvp/(\d+)/roommate/$', roommate),
    (r'^rsvp/(\d+)/roommate/show/$', roommate_detail),
    (r'^rsvp/(\d+)/ignite/$', ignite),
    (r'^rsvp/(\d+)/ignite/show/$', ignite_detail),
    (r'^rsvp/(\d+)/stipend/$', stipend),
    (r'^rsvp/(\d+)/stipend/show/$', stipend_detail),
    (r'^rsvp/(\d+)/logistics/$', invite_logistics),
    (r'^guest/(\d+)/$', guest_invite),
)
