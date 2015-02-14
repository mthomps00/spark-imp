from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from rsvp.models import *
from nod.models import *
import random, csv, datetime, unicodecsv
from urllib import urlopen

nominees_sheet = 'http://sparkcamp.com/wp-content/uploads/2015/02/feb13_import.csv'
nominees = csv.DictReader(urlopen(nominees_sheet))
camp = Camp.objects.get(theme='Giving')
round, vroundcreated = VotingRound.objects.get_or_create(short_name='Second round',camp=camp)
Amy = User.objects.get(username='Amy')
awballot, awballotcreated = Ballot.objects.get_or_create(voter=Amy,voting_round=round)
Amanda = User.objects.get(username='Amanda')
amballot, amballotcreated = Ballot.objects.get_or_create(voter=Amanda,voting_round=round)
Andy = User.objects.get(username='Andy')
apballot, apballotcreated = Ballot.objects.get_or_create(voter=Andy,voting_round=round)
Matt = User.objects.get(username='Matt')
mtballot, mtballotcreated = Ballot.objects.get_or_create(voter=Matt,voting_round=round)

for row in nominees:
    first_name = row['First name']
    last_name = row['Last name']
    combinedname = first_name + last_name
    username = slugify(combinedname)
    if User.objects.filter(username=username):
        user = User.objects.get(username=username)
        user.first_name = first_name
        user.last_name = last_name
    else:
        user, usercreated = User.objects.update_or_create(username=username,first_name=first_name,last_name=last_name)
    user.email = row['Email address']
    sparkprofile, profilecreated = SparkProfile.objects.get_or_create(user=user)
    sparkprofile.secondary_email = row['Secondary email']
    sparkprofile.twitter = row['Twitter']
    sparkprofile.url = row['URL']
    if row['POC'] == 'TRUE':
        sparkprofile.poc = True
    else:
        sparkprofile.poc = False
    if row['Woman'] == 'TRUE':
        sparkprofile.woman = True
    else:
        sparkprofile.woman = False
    if row['Journo'] == 'TRUE':
        sparkprofile.journo = True
    else:
        sparkprofile.journo = False
    sparkprofile.job_title = row['Job title']
    sparkprofile.phone = row['Phone']
    sparkprofile.employer = row['Organization']
    user.save()
    sparkprofile.save()
    
    nominators_list = row['Nominated by']
    nominators = [nominator.strip() for nominator in nominators_list.split(',')]
    for nominator in nominators:
        comboname = nominator.replace(" ", "")
        noddername = slugify(comboname)
        person, personcreated = User.objects.get_or_create(username=noddername)
        reason = row['Comments/notes']
        nomination, nodcreated = Nomination.objects.update_or_create(user=user,nominated_by=person,camp=camp,reason=reason)
    
    tags_list = row['Tags']
    tags = [tag.strip() for tag in tags_list.split(',')]
    for tag in tags:
        t, tagcreated = Tag.objects.get_or_create(name=tag)
        user.tags.add(t)
        
    '''if row['AM votes'] != '':
        amvalue = int(float(row['AM votes']))
        amvote, amcreated = Vote.objects.update_or_create(user=user,value=amvalue,ballot=amballot)
    if row['AP votes'] != '':
        apvalue = int(float(row['AP votes']))
        apvote, apcreated = Vote.objects.update_or_create(user=user,value=apvalue,ballot=apballot)
    if row['AW votes'] != '':
        awvalue = int(float(row['AW votes']))
        awvote, awcreated = Vote.objects.update_or_create(user=user,value=awvalue,ballot=awballot)
    if row['MT votes'] != '':
        mtvalue = int(float(row['MT votes']))
        mtvote, mtcreated = Vote.objects.update_or_create(user=user,value=mtvalue,ballot=mtballot)'''
        
    print user,sparkprofile