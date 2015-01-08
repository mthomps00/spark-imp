# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nod', '0013_nomination_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(related_query_name=b'vote', related_name=b'votes', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'ballot')]),
        ),
        migrations.RemoveField(
            model_name='vote',
            name='nomination',
        ),
        migrations.AlterUniqueTogether(
            name='nomination',
            unique_together=set([('nominated_by', 'camp', 'user')]),
        ),
    ]
