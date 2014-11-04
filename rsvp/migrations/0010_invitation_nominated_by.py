# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0009_auto_20141102_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='nominated_by',
            field=models.CharField(max_length=60, null=True, blank=True),
            preserve_default=True,
        ),
    ]
