from django import forms
from django.forms import ModelForm
from rsvp.models import *

# Model Forms
class RSVPForm(ModelForm):
    class Meta:
        model = Invitation
        fields = ('status',)
    
class RoommateForm(ModelForm):
    class Meta:
        model = Roommate
        exclude = ('invitation',)
        
class IgniteForm(ModelForm):
    class Meta:
        model = Ignite
        exclude = ('invitation',)
        
class StipendForm(ModelForm):
    class Meta:
        model = Stipend
        exclude = ('invitation',)
        
class InviteDetailForm(ModelForm):
    class Meta:
        model = Invitation
        fields = ('dietary', 'arrival_time', 'departure_time', 'hotel_booked')

"""
class StatusForm(ModelForm):
    class Meta:
        model = Invitation
        
    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        if self.instance.status == 'Y':
            STATUS_CHOICES = (
                ('Y', 'I\'m still coming to Spark Camp'),
                ('C', 'I\'m afraid I have to cancel'),
            )
        elif self.instance.status == 'N' or self.instance.status == 'C':
            STATUS_CHOICES = (
                ('N', 'I still can\'t make it to Spark Camp'),
                ('Y', 'I\'ll be able to make it to Spark Camp after all'),
            )
        elif self.instance.status == 'W':
            STATUS_CHOICES = (
                ('N', 'I can\'t make it to Spark Camp'),
                ('W', 'I\'d like to be on the waitlist'),
            )
        else:
            STATUS_CHOICES = (
                ('', '-- Please select your RSVP --'),
                ('Y', 'I\'m coming to Spark Camp'),
                ('N', 'I can\'t make it to Spark Camp'),
                ('M', 'I might be able to come, but need more time'),
            )
        self.fields['status'].choices = STATUS_CHOICES
"""

# Custom forms
class ResponseForm(forms.Form):
    RSVP_CHOICES = (
        ('', '-- Please select your RSVP --'),
        ('Y', 'I\'m coming to Spark Camp'),
        ('N', 'I can\'t make it to Spark Camp'),
        ('M', 'I might be able to come, but need more time'),
    )
    status = forms.ChoiceField(choices=RSVP_CHOICES)
    
class UpdateForm(forms.Form):
    UPDATE_CHOICES = (
        ('Y', 'I\'m still coming to Spark Camp'),
        ('C', 'I\'m afraid I have to cancel'),
    )
    status = forms.ChoiceField(choices=UPDATE_CHOICES)

class WaitlistForm(forms.Form):
    WAITLIST_CHOICES = (
        ('N', 'I can\'t make it to Spark Camp'),
        ('W', 'I\'d like to be on the waitlist'),
    )
    status = forms.ChoiceField(choices=WAITLIST_CHOICES)
    
class ResurrectForm(forms.Form):
    RESURRECT_CHOICES = (
        ('N', 'I still can\'t make it to Spark Camp'),
        ('Y', 'I\'ll be able to make it to Spark Camp after all'),
    )
    status = forms.ChoiceField(choices=RESURRECT_CHOICES)
    
