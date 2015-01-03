# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomination',
            name='self_nomination',
            field=models.BooleanField(default=False),
        ),
    ]
