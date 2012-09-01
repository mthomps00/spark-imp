from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from rsvp.models import *

class StipendInline(admin.TabularInline):
    model = Stipend

class IgniteInline(admin.TabularInline):
    model = Ignite
    
class RoommateInline(admin.TabularInline):
    model = Roommate

class SessionInline(admin.TabularInline):
    model = Session

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('user', 'camp', 'status', 'expires', 'rand_id')
    list_filter = ('camp',)
    search_fields = ('user',)
    
    inlines = [
        StipendInline,
        IgniteInline,
        RoommateInline,
        SessionInline,
    ]

class InvitationInline(admin.TabularInline):
    model = Invitation
    fields = ('user', 'status', 'type', 'expires')
    extra = 20

class CampAdmin(admin.ModelAdmin):
    inlines = [
        InvitationInline,
    ]

admin.site.register(Camp, CampAdmin)
admin.site.register(Invitation, InvitationAdmin)

# SparkProfile-specific commands. Leave these last, 'cause the order matters.
class SparkProfileInline(admin.StackedInline):
    model = SparkProfile
    
class UserProfileAdmin(UserAdmin):
    inlines = [
        SparkProfileInline,
    ]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
