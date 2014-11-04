# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0003_auto_20141026_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='faq_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='custom_message',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(default=b'Q', max_length=1, choices=[(b'Q', b'Invitation not yet sent'), (b'P', b'Awaiting a response'), (b'Y', b'Attendance confirmed'), (b'I', b'Registration incomplete'), (b'N', b"Can't make it"), (b'C', b'Had to cancel'), (b'X', b'No response'), (b'Z', b'No show'), (b'W', b'On the waitlist'), (b'M', b'Maybe')]),
        ),
    ]
