# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0005_camp_banner_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='display_name',
            field=models.CharField(max_length=60, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='camp',
            name='short_name',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
