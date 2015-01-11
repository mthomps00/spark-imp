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
    success = models.BooleanField(default=False)
    
    def __unicode__(self):
        name = self.user.first_name + ' ' + self.user.last_name + ' nomination'
        if self.camp:
            name += ' for ' + self.camp.display_name
        if self.nominated_by:
            name += ' (by ' + self.nominated_by.first_name + ' ' + self.nominated_by.last_name + ')'
        return name
    
    class Meta:
        unique_together = ('nominated_by', 'camp', 'user')

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(User, related_name="tags", related_query_name="tag")
    
    def __unicode__(self):
        return self.name

    
class VotingRound(models.Model):
    camp = models.ForeignKey(Camp)
    short_name = models.CharField(max_length=25, default='New voting round')
    description = models.TextField(blank=True, null=True)
    num_votes = models.PositiveSmallIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.short_name

class Ballot(models.Model):
    voter = models.ForeignKey(User, related_name="ballots", related_query_name="ballot")
    voting_round = models.ForeignKey(VotingRound)    

    def __unicode__(self):
        name = u'{0}: {1}'.format(self.voting_round.short_name, self.voter.username)
        return name
    
    class Meta:
        unique_together = ('voter', 'voting_round')
    
class Vote(models.Model):
    user = models.ForeignKey(User, related_name="votes", related_query_name="vote")
    value = models.PositiveSmallIntegerField(default=0)
    ballot = models.ForeignKey(Ballot)
    comment = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        name = u'{0} ({1}): {2} votes for {3} {4}'.format(self.ballot.voting_round.short_name, self.ballot.voter.username, self.value, self.user.first_name, self.user.last_name)
        return name

    class Meta:
        unique_together = ('user', 'ballot')
