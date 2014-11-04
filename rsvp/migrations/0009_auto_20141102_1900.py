# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0008_auto_20141102_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='capacity',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='camp',
            name='ticket_cost',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='special_cost',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
