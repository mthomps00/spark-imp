# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0024_camp_mailchimp_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparkprofile',
            name='mailchimp_id',
            field=models.CharField(max_length=140, null=True, blank=True),
            preserve_default=True,
        ),
    ]
