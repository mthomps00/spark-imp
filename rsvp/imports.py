from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from rsvp.models import *
from nod.models import *
import random, csv, datetime, unicodecsv
from urllib import urlopen

camps_sheet = 'http://sparkcamp.com/wp-content/uploads/2015/01/camps.csv'
camps = csv.DictReader(urlopen(camps_sheet))

campers_sheet = 'http://sparkcamp.com/wp-content/uploads/2015/01/campers.csv'
campers = csv.DictReader(urlopen(campers_sheet))

invites_sheet = 'http://sparkcamp.com/wp-content/uploads/2015/01/invites.csv'
invites = csv.DictReader(urlopen(invites_sheet))

for row in camps:
    theme = row['Theme']
    description = row['Description']
    logistics = row['Logistics']
    hotel = row['Hotel']
    hotel_link = row['Hotel link']
    hotel_code = row['Hotel code']
    venue = row['Venue']
    venue_address = row['Venue address']
    if row['Ignite'] == 'False':
        ignite = False
    else:
        ignite = True
    if row['Stipends'] == 'False':
        stipends = False
    else:
        stipends = True
    spreadsheet_url = row['Spreadsheet URL']
    mailchimp_list = row['Mailchimp list']

    camp, created = Camp.objects.get_or_create(theme=theme,description=description,logistics=logistics,hotel=hotel,hotel_link=hotel_link,hotel_code=hotel_code,venue=venue,venue_address=venue_address,ignite=ignite,stipends=stipends,spreadsheet_url=spreadsheet_url,mailchimp_list=mailchimp_list)
    print camp
    
for row in campers:
    username = row['Username']
    first_name = row['First name']
    last_name = row['Last name']
    email = row['Email address']
    secondary_email = row['Secondary email']
    twitter = row['Twitter']
    url = row['URL']
    if row['POC'] == 'False':
        poc = False
    else:
        poc = True
    if row['Woman'] == 'False':
        woman = False
    else:
        woman = True
    if row['Journo'] == 'False':
        journo = False
    else:
        journo = True
    dietary = row['Dietary preferences']
    job_title = row['Job title']
    phone = row['Phone']
    employer = row['Organization']
    bio = row['Bio']

    user, created = User.objects.update_or_create(username=username,first_name=first_name,last_name=last_name,email=email)
    sparkprofile = SparkProfile.objects.filter(user=user).update(secondary_email=secondary_email,twitter=twitter,url=url,poc=poc,woman=woman,journo=journo,dietary=dietary,job_title=job_title,phone=phone,employer=employer,bio=bio)
    print user,sparkprofile
    
for row in invites:
    status = row['Status']
    type = row['Type']
    if row['Plus one'] == 'False':
        plus_one = False
    else:
        plus_one = True
    if row['Hotel booked'] == 'False':
        hotel_booked = False
    else:
        hotel_booked = True
    expires = row['Expires']
    user = User.objects.get(username=row['User'])
    camp = Camp.objects.get(theme=row['Camp'])
    rand_id = row['Rand_ID']

    invite, created = Invitation.objects.update_or_create(user=user,camp=camp,status=status,type=type,plus_one=plus_one,expires=expires,rand_id=rand_id,hotel_booked=hotel_booked)
    print invite