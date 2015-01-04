# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0010_auto_20150104_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='value',
            field=models.PositiveSmallIntegerField(default=False),
        ),
    ]
