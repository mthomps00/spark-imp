# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rsvp.thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0018_auto_20150104_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sparkprofile',
            name='headshot',
        ),
        migrations.AddField(
            model_name='sparkprofile',
            name='photo',
            field=rsvp.thumbs.ImageWithThumbsField(null=True, upload_to=b'headshot', blank=True),
            preserve_default=True,
        ),
    ]
