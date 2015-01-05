# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0016_auto_20150104_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparkprofile',
            name='image',
            field=models.ImageField(null=True, upload_to=b'headshots/', blank=True),
            preserve_default=True,
        ),
    ]
