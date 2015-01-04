from django.contrib import admin
from django.contrib.auth.models import User
from nod.models import *

# Register your models here.

admin.site.register(Nomination)
admin.site.register(Tag)
admin.site.register(VotingRound)
admin.site.register(Ballot)
admin.site.register(Vote)
