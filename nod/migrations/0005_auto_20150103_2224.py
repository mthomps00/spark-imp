# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0004_votinground_short_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ballot',
            unique_together=set([('voter', 'voting_round')]),
        ),
    ]
