# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0026_camp_mailchimp_setup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camp',
            name='mailchimp_setup',
        ),
        migrations.AddField(
            model_name='camp',
            name='hotel_address',
            field=models.CharField(max_length=140, null=True, blank=True),
            preserve_default=True,
        ),
    ]
