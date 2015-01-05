# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0017_sparkprofile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sparkprofile',
            name='image',
        ),
        migrations.AlterField(
            model_name='sparkprofile',
            name='headshot',
            field=models.ImageField(null=True, upload_to=b'headshots/', blank=True),
        ),
    ]
