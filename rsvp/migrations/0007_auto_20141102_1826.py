# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0006_auto_20141102_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camp',
            name='hotel',
            field=models.CharField(max_length=60, blank=True),
        ),
        migrations.AlterField(
            model_name='camp',
            name='hotel_code',
            field=models.CharField(max_length=60, verbose_name=b'Hotel promotion code', blank=True),
        ),
        migrations.AlterField(
            model_name='camp',
            name='venue',
            field=models.CharField(max_length=60, blank=True),
        ),
    ]
