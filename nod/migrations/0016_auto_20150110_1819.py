# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0015_auto_20150110_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nomination',
            old_name='nominator',
            new_name='nominated_by',
        ),
        migrations.RenameField(
            model_name='nomination',
            old_name='nominee',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='nomination',
            unique_together=set([('nominated_by', 'camp', 'user')]),
        ),
    ]
