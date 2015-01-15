from django.contrib import admin
from django.contrib.auth.models import User
from nod.models import *

class VoteInline(admin.TabularInline):
    model = Vote
    
class BallotAdmin(admin.ModelAdmin):
    model = Ballot
  
    inlines = [
      VoteInline,
    ]

# Register your models here.

admin.site.register(Nomination)
admin.site.register(Tag)
admin.site.register(VotingRound)
admin.site.register(Ballot, BallotAdmin)
admin.site.register(Vote)
