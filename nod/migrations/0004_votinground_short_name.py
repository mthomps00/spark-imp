# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0003_auto_20150103_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='votinground',
            name='short_name',
            field=models.CharField(default=b'New voting round', max_length=25),
            preserve_default=True,
        ),
    ]
