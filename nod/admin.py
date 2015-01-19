from django.contrib import admin
from django.contrib.auth.models import User
from nod.models import *

class VoteInline(admin.TabularInline):
    model = Vote
    ordering = ['-value', 'user']
    
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
admin.site.register(Vote)
