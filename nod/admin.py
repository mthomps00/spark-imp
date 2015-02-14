from django.contrib import admin
from django.contrib.auth.models import User
from nod.models import *

class VoteInline(admin.TabularInline):
    model = Vote
    ordering = ['-value', 'user']

class VoteAdmin(admin.ModelAdmin):
    model = Vote
    
    def user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    
    search_fields = ('ballot__voter__username', 'ballot__voter__first_name', 'ballot__voter__last_name', 'user__username')
    list_display = ('user_name', 'value', 'ballot', 'comment')
    
class BallotAdmin(admin.ModelAdmin):
    model = Ballot
  
    inlines = [
      VoteInline,
    ]

class NodAdmin(admin.ModelAdmin):
    model = Nomination
    search_fields = ('user__username', 'user__first_name', 'user__last_name',)
    list_display = ('user', 'reason', 'description',)
    list_filter = ('camp', 'success',)
    ordering = ['user']
    
# Register your models here.

admin.site.register(Nomination, NodAdmin)
admin.site.register(Tag)
admin.site.register(VotingRound)
admin.site.register(Ballot, BallotAdmin)
admin.site.register(Vote, VoteAdmin)
