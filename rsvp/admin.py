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
    list_display = ('name', 'camp', 'status', 'expires', 'custom_message', 'nominated_by', 'contact', 'rand_id')
    list_filter = ('camp', 'status',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',)
    ordering = ('user__last_name',)
    actions = ('confirm', 'cant_make', 'cancel', 'no_response', 'no_show', 'waitlist', 'maybe', 'set_self_as_contact')
    
    def name(self, obj):
        return ('%s %s' % (obj.user.first_name, obj.user.last_name))
    name.short_description = 'Name'
    name.admin_order_field = 'user__last_name'
    
    def confirm(modeladmin, request, queryset):
        queryset.update(status='Y')
    confirm.short_description = "Change to 'Attendance confirmed'"
    
    def cant_make(modeladmin, request, queryset):
        queryset.update(status='N')
    cant_make.short_description = "Change to 'Can\'t make it'"
    
    def cancel(modeladmin, request, queryset):
        queryset.update(status='C')
    cancel.short_description = "Change to 'Had to cancel'"
    
    def no_response(modeladmin, request, queryset):
        queryset.update(status='X')
    no_response.short_description = "Change to 'No response'"
    
    def no_show(modeladmin, request, queryset):
        queryset.update(status='Z')
    no_show.short_description = "Change to 'No show'"
    
    def waitlist(modeladmin, request, queryset):
        queryset.update(status='W')
    waitlist.short_description = "Change to 'On the waitlist'"
    
    def maybe(modeladmin, request, queryset):
        queryset.update(status='Y')
    maybe.short_description = "Change to 'Maybe'"
    
    def set_self_as_contact(modeladmin, request, queryset):
        queryset.update(contact=request.user)
    set_self_as_contact.short_description = "Set yourself as the contact"
    
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
    pass

admin.site.register(Camp, CampAdmin)
admin.site.register(Invitation, InvitationAdmin)

# SparkProfile-specific commands. Leave these last, 'cause the order matters.
class SparkProfileInline(admin.StackedInline):
    model = SparkProfile
    max_num = 1
    can_delete = False

class SparkProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'poc', 'woman', 'journo',)
    list_filter = ('user__invitation__camp',)
    actions = ('make_poc', 'make_woman', 'make_journo', 'un_poc', 'un_woman', 'un_journo',)

    def name(self, obj):
        return ('%s %s' % (obj.user.first_name, obj.user.last_name))
    name.short_description = 'Name'
    name.admin_order_field = 'user__last_name'
    
    def make_poc(modeladmin, request, queryset):
        queryset.update(poc=True)
    make_poc.short_description = "Selected individuals are people of color"

    def make_woman(modeladmin, request, queryset):
        queryset.update(woman=True)
    make_woman.short_description = "Selected individuals are women"

    def make_journo(modeladmin, request, queryset):
        queryset.update(journo=True)
    make_journo.short_description = "Selected individuals are journalists"
    
    def un_poc(modeladmin, request, queryset):
        queryset.update(poc=False)
    un_poc.short_description = "Selected individuals are not people of color"

    def un_woman(modeladmin, request, queryset):
        queryset.update(woman=False)
    un_woman.short_description = "Selected individuals are not women"

    def un_journo(modeladmin, request, queryset):
        queryset.update(journo=False)
    un_journo.short_description = "Selected individuals are not journalists"
    
admin.site.register(SparkProfile, SparkProfileAdmin)

class UserProfileAdmin(UserAdmin):
   def add_view(self, *args, **kwargs):
      self.inlines = []
      return super(UserAdmin, self).add_view(*args, **kwargs)

   def change_view(self, *args, **kwargs):
      self.inlines = [SparkProfileInline]
      return super(UserAdmin, self).change_view(*args, **kwargs)

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
