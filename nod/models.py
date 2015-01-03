from django.contrib.auth.models import User
from django.db import models
from rsvp.models import Camp, SparkProfile, Invitation

# Create your models here.

class Nomination(models.Model):
    user = models.ForeignKey(User, related_name="nominations", related_query_name="nomination")
    nominated_by = models.ForeignKey(User, null=True)
    camp = models.ForeignKey(Camp, null=True)
    reason = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    self_nomination = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(User, related_name="tags", related_query_name="tag")
    
class VotingRound(models.Model):
    camp = models.ForeignKey(Camp)
    description = models.TextField(blank=True, null=True)
    num_votes = models.PositiveSmallIntegerField()

class Ballot(models.Model):
    user = models.ForeignKey(User, related_name="ballots", related_query_name="ballot")
    voting_round = models.ForeignKey(VotingRound)
    
class Vote(models.Model):
    nomination = models.ForeignKey(Nomination)
    value = models.PositiveSmallIntegerField()
    ballot = models.ForeignKey(Ballot)