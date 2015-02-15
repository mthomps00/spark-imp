from django import forms
from django.forms import ModelForm
from rsvp.models import *
from nod.models import *

def camp_choices():
    camps = Camp.objects.all()
    CAMP_CHOICES = [
      ('N', 'Any Spark Camp event'),
    ]
    for camp in camps:
        CAMP_CHOICES.append(tuple((camp.short_name, camp.display_name)))
    return tuple(CAMP_CHOICES)

class NominationForm(forms.Form):
    user_first_name = forms.CharField(max_length=30, required=True, label="Your first name")
    user_last_name = forms.CharField(max_length=30, required=True, label="Your last name")
    user_email = forms.EmailField(required=True, label="Your email address")
    user_alum = forms.BooleanField(required=False, label="Alum status", help_text="Check here if you've been invited to a Spark Camp event.")
    first_name = forms.CharField(max_length=30, required=True, label="Nominee's first name")
    last_name = forms.CharField(max_length=30, required=True, label="Nominee's last name")
    email = forms.EmailField(required=True, label="Nominee email address", help_text="Nominee's best email address")
    reason = forms.CharField(required=True, label="Reason", help_text="In a short paragraph, tell us why you think this person would be a good fit.", widget=forms.Textarea)
    description = forms.CharField(required=True, label="Description", help_text="Give us a quick description of this person.", widget=forms.Textarea)
    employer = forms.CharField(required=True, max_length=140, label="Organization", help_text="What organization does this person work for?")
    job_title = forms.CharField(required=True, max_length=140, label="Title", help_text="What is this person's title?")
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('N', 'Neither male nor female / Prefer not to say'),
    )
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES, label="Gender", help_text="What gender does this person identify as?")
    poc = forms.BooleanField(required=False, label="POC", help_text="Check this box if your nominee is a person of color.")
    camp = forms.ChoiceField(required=False, choices=camp_choices(), label="Camp", help_text="Got a particular event in mind?")
    secondary_email = forms.EmailField(required=False, label="Secondary email", help_text="If this person has an assistant or secondary email address, please list that here.")
