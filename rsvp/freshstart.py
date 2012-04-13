#!/usr/bin/env python

from rsvp.models import *
import datetime

def make_camp(c):
    camp = Camp(theme=c['theme'], description=c['description'], start_date=c['start_date'], end_date=c['end_date'], hotel=c['hotel'])
    camp.save()

def make_camper(u):
    user = User(username=u['username'], first_name=u['first_name'], last_name=u['last_name'], is_staff=u['is_staff'])
    user.set_password(u['password'])
    user.save()

def make_camper_profile(u):
    user = User.objects.get(username=u['username'])
    profile = SparkProfile.objects.get(user=user.id)
    profile.employer = u['employer']
    profile.first_name = u['first_name']
    profile.last_name = u['last_name']
    profile.job_title = u['job_title']
    profile.poc = u['poc']
    profile.woman = u['woman']
    profile.journo = u['journo']
    profile.save()

def make_full_camper(u):
     make_camper(u)  
     make_camper_profile(u)
     
def make_invitation(u, c):
    user = User.objects.get(username=u)
    camp = Camp.objects.get(theme=c)
    
    # calculate default expiration date
    today = datetime.date.today()
    two_weeks = datetime.timedelta(days=14)
    expires = today + two_weeks

    invite = Invitation(user=user, camp=camp, status='P', type='G', plus_one=False, expires=expires)
    invite.save()

Jenny = {
     'username': 'Jenny',
     'first_name': 'Jenny',
     'last_name': 'Lee',
     'password': 'sparkcandy',
     'is_staff': True,
     'employer': 'self',
     'job_title': 'nomad/board member',
     'poc': True,
     'woman': True,
     'journo': True,
}

Andy = {
     'username': 'Andy',
     'first_name': 'Andy',
     'last_name': 'Pergam',
     'password': 'sparkcandy',
     'is_staff': True,
     'employer': 'Washington Post',
     'job_title': 'Director of Video',
     'poc': False,
     'woman': False,
     'journo': True,
}

Amanda = {
     'username': 'Amanda',
     'first_name': 'Amanda',
     'last_name': 'Michel',
     'password': 'sparkcandy',
     'is_staff': True,
     'employer': 'The Guardian',
     'job_title': 'Open Editor',
     'poc': False,
     'woman': True,
     'journo': True,
}

Amy = {
     'username': 'Amy',
     'first_name': 'Amy',
     'last_name': 'Webb',
     'password': 'sparkcandy',
     'is_staff': True,
     'employer': 'Webbmedia Group',
     'job_title': 'CEO',
     'poc': False,
     'woman': True,
     'journo': True,
}

Sam = {
     'username': 'Sam',
     'first_name': 'Sam',
     'last_name': 'Waldbuch',
     'password': 'sparkcandy',
     'is_staff': False,
     'employer': 'SeanCody.com',
     'job_title': 'pornjourno',
     'poc': False,
     'woman': False,
     'journo': True,
 }

Data = {
    'theme': 'Data',
    'description': 'Spark Camp Data is all about how data is fun and only data scientists should have fun with it!',
    'start_date': datetime.date(2012, 1, 13),
    'end_date': datetime.date(2012, 1, 15),
    'hotel': 'The Driskill',
}

Money = {
    'theme': 'Money',
    'description': 'Spark Camp is an atypical unconference featuring a diverse, highly curated mix of individuals from inside and outside of the news industry. Each Camp is unique - with its own set of invitees and its own particular theme. The theme for July\'s event at Harvard\'s Walter Lippman House is "Money." In attendance will be founders, funders, fundraisers, CEOs, CFOs, quants, and many others whose jobs revolve around running businesses and raising revenue.',
    'start_date': datetime.date(2012, 7, 20),
    'end_date': datetime.date(2012, 7, 22),
    'hotel': 'The Inn at Harvard',
    'venue': 'Walter Lippman House',
}

camps = (Money, Data)
users = (Andy, Amanda, Amy, Jenny, Sam)

for camp in camps:
    make_camp(camp)
    
for user in users:
    make_full_camper(user)
    make_invitation(user['username'], 'Money')
