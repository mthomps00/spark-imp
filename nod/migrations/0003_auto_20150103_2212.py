# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0002_auto_20150103_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ballot',
            old_name='user',
            new_name='voter',
        ),
        migrations.AlterField(
            model_name='vote',
            name='nomination',
            field=models.ForeignKey(related_query_name=b'vote', related_name=b'votes', to='nod.Nomination'),
        ),
    ]
