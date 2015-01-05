# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0019_auto_20150104_1929'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sparkprofile',
            old_name='photo',
            new_name='headshot',
        ),
    ]
