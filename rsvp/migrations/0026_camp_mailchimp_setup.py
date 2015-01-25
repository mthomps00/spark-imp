# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0025_sparkprofile_mailchimp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='mailchimp_setup',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
