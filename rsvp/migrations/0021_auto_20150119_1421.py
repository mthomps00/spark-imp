# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0020_auto_20150104_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparkprofile',
            name='headshot',
            field=models.ImageField(null=True, upload_to=b'headshot', blank=True),
        ),
    ]
