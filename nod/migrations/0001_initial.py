# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0013_auto_20141106_2129'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(related_query_name=b'ballot', related_name=b'ballots', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nomination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('self_nomination', models.BooleanField()),
                ('camp', models.ForeignKey(to='rsvp.Camp', null=True)),
                ('nominated_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_query_name=b'nomination', related_name=b'nominations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('user', models.ManyToManyField(related_query_name=b'tag', related_name=b'tags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.PositiveSmallIntegerField()),
                ('ballot', models.ForeignKey(to='nod.Ballot')),
                ('nomination', models.ForeignKey(to='nod.Nomination')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VotingRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('num_votes', models.PositiveSmallIntegerField()),
                ('camp', models.ForeignKey(to='rsvp.Camp')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ballot',
            name='voting_round',
            field=models.ForeignKey(to='nod.VotingRound'),
            preserve_default=True,
        ),
    ]
