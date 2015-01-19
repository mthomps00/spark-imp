# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0021_auto_20150119_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sparkprofile',
            name='has_headshot',
        ),
    ]
