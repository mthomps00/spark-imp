# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0012_auto_20150104_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='success',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
