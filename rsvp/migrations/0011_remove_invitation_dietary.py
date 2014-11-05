# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0010_invitation_nominated_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='dietary',
        ),
    ]
