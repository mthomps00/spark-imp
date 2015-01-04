# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0006_auto_20150103_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='votinground',
            name='created_on',
            field=models.DateTimeField(default=datetime.date(2015, 1, 3), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='votinground',
            name='modified',
            field=models.DateTimeField(default=datetime.date(2015, 1, 3), auto_now_add=True),
            preserve_default=False,
        ),
    ]
