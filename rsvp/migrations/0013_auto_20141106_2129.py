# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0012_auto_20141105_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='confirmation_email',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='comp_ticket',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
