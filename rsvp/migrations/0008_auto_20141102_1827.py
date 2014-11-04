# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0007_auto_20141102_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='city',
            field=models.CharField(max_length=60, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='camp',
            name='state',
            field=models.CharField(max_length=2, null=True, blank=True),
            preserve_default=True,
        ),
    ]
