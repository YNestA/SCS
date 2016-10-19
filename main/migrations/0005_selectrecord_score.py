# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_droprecord_systemnotify'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectrecord',
            name='score',
            field=models.CharField(default=b'', max_length=10, blank=True),
        ),
    ]
