# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('theme', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('logistics', models.TextField(blank=True)),
                ('hotel', models.CharField(max_length=30, blank=True)),
                ('hotel_link', models.URLField(blank=True)),
                ('hotel_code', models.CharField(max_length=30, verbose_name=b'Hotel promotion code', blank=True)),
                ('hotel_deadline', models.DateField(null=True, blank=True)),
                ('venue', models.CharField(max_length=30, blank=True)),
                ('venue_address', models.CharField(max_length=140, blank=True)),
                ('ignite', models.BooleanField(default=False)),
                ('stipends', models.BooleanField(default=False)),
                ('talk', models.BooleanField(default=False)),
                ('spreadsheet_url', models.URLField(blank=True)),
                ('mailchimp_list', models.CharField(max_length=140, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ignite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b"What's the title of your proposed talk?", max_length=140)),
                ('experience', models.CharField(help_text=b'Have you done an Ignite or similar presentation before?', max_length=1, choices=[(b'Y', b"Yep, I'm an Ignite pro."), (b'M', b"I think I've done something similar."), (b'N', b"No, but I think I'll be OK.")])),
                ('description', models.TextField(help_text=b"What's your talk about? Give us a little detail.")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Q', max_length=1, choices=[(b'Q', b'Invitation not yet sent'), (b'P', b'Awaiting a response'), (b'Y', b'Attendance confirmed'), (b'N', b"Can't make it"), (b'C', b'Had to cancel'), (b'X', b'No response'), (b'Z', b'No show'), (b'W', b'On the waitlist'), (b'M', b'Maybe')])),
                ('type', models.CharField(default=b'G', max_length=1, choices=[(b'G', b'Guest'), (b'S', b'Sponsor'), (b'H', b'Host'), (b'A', b'Administrative Support / Staff')])),
                ('plus_one', models.BooleanField(default=False)),
                ('expires', models.DateField(null=True, blank=True)),
                ('rand_id', models.CharField(unique=True, max_length=8, editable=False)),
                ('dietary', models.CharField(default=b'None', help_text=b'Please note any dietary preferences here.', max_length=140, verbose_name=b'Dietary needs', blank=True)),
                ('arrival_time', models.DateTimeField(help_text=b"Tell us the time you'll be arriving at Spark Camp (format: 2006-10-25 14:30).", null=True, blank=True)),
                ('departure_time', models.DateTimeField(help_text=b"Tell us the time you'll be leaving Spark Camp (format: 2006-10-25 14:30).", null=True, blank=True)),
                ('hotel_booked', models.BooleanField(default=False, help_text=b"Check here if you've taken care of your hotel room.")),
                ('camp', models.ForeignKey(to='rsvp.Camp')),
                ('inviter', models.ForeignKey(blank=True, to='rsvp.Invitation', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlusOne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=75)),
                ('employer', models.CharField(help_text=b"Person's place of work", max_length=140, blank=True)),
                ('job_title', models.CharField(help_text=b"Person's job title", max_length=140, blank=True)),
                ('reason', models.TextField(help_text=b'Tell us why this person would be great for Spark Camp.')),
                ('invitation', models.ForeignKey(to='rsvp.Invitation', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Roommate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.CharField(help_text=b"What's your sex?", max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other / Prefer not to say')])),
                ('roommate', models.CharField(help_text=b'What sex are you comfortable rooming with?', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'A', b'Comfortable with anyone')])),
                ('more', models.CharField(help_text=b'Anything else we should know?', max_length=140, blank=True)),
                ('invitation', models.ForeignKey(to='rsvp.Invitation', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Suggest a name for this session', max_length=140)),
                ('description', models.TextField(help_text=b'What do you expect the session to be about?')),
                ('invitation', models.ForeignKey(to='rsvp.Invitation', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SparkProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.CharField(help_text=b'Tell us your bio. Keep it Twitter-length.', max_length=140, blank=True)),
                ('employer', models.CharField(help_text=b'The name of your primary employer.', max_length=140, blank=True)),
                ('twitter', models.CharField(help_text=b"What's your Twitter username?", max_length=20, blank=True)),
                ('url', models.URLField(help_text=b'Link to your personal site or profile.', blank=True)),
                ('email', models.EmailField(help_text=b'Preferred email address.', max_length=75, blank=True)),
                ('secondary_email', models.EmailField(help_text=b'Alternate (or admin assistant) email address.', max_length=75, blank=True)),
                ('job_title', models.CharField(help_text=b'Your job title.', max_length=140, blank=True)),
                ('phone', models.CharField(help_text=b'Preferred phone number for us to reach you.', max_length=30, blank=True)),
                ('dietary', models.CharField(default=b'None', help_text=b'Please note any food allergies or restrictions here.', max_length=140, verbose_name=b'Dietary needs', blank=True)),
                ('poc', models.BooleanField(default=False, verbose_name=b'Person of color')),
                ('woman', models.BooleanField(default=False)),
                ('journo', models.BooleanField(default=False, help_text=b'Works predominantly in the news industry?')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stipend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost_estimate', models.IntegerField(help_text=b"How much do you estimate air and ground transportation will cost? Don't include lodging and meals. (Just numbers, no dollar signs or symbols.)", max_length=140, null=True, blank=True)),
                ('employer_subsidized', models.CharField(default=b'U', help_text=b'Will your employer provide any funds towards travel?', max_length=1, verbose_name=b'Employer will cover some costs', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b'U', b'Unsure')])),
                ('employer_percentage', models.IntegerField(help_text=b'What percentage of the cost will your employer cover? (Just numbers, no dollar signs or symbols.)', null=True, blank=True)),
                ('invitee_percentage', models.IntegerField(help_text=b'What percentage of the cost can you cover yourself? (Just numbers, no dollar signs or symbols.)', null=True, blank=True)),
                ('details', models.TextField(help_text=b'Please explain any other factors that would assist us in processing this request.', blank=True)),
                ('invitation', models.ForeignKey(to='rsvp.Invitation', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('user', 'camp')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='invitation',
            order_with_respect_to='user',
        ),
        migrations.AddField(
            model_name='ignite',
            name='invitation',
            field=models.ForeignKey(to='rsvp.Invitation', unique=True),
            preserve_default=True,
        ),
    ]
