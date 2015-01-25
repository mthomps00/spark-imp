# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0023_invitation_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='mailchimp_code',
            field=models.CharField(max_length=5, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
