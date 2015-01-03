# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0013_auto_20141106_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camp',
            name='faq_url',
        ),
        migrations.AddField(
            model_name='camp',
            name='faq',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
