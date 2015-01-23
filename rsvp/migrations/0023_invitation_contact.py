# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rsvp', '0022_remove_sparkprofile_has_headshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='contact',
            field=models.ForeignKey(related_name=b'contact', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
