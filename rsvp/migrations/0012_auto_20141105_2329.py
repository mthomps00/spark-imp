# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0011_remove_invitation_dietary'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='cancel_by',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sparkprofile',
            name='has_headshot',
            field=models.BooleanField(default=False, help_text=b"Check this if you've sent your headshot to sparkcampphotos@gmail.com.", verbose_name=b'Headshot sent'),
        ),
    ]
