# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nod', '0014_auto_20150106_0703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nomination',
            old_name='nominated_by',
            new_name='nominator',
        ),
        migrations.RenameField(
            model_name='nomination',
            old_name='user',
            new_name='nominee',
        ),
        migrations.AlterUniqueTogether(
            name='nomination',
            unique_together=set([('nominator', 'camp', 'nominee')]),
        ),
    ]
