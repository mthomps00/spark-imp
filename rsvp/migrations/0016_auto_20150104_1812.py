# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0015_sparkprofile_headshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparkprofile',
            name='headshot',
            field=models.FileField(null=True, upload_to=b'headshots/', blank=True),
        ),
    ]
