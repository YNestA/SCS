# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20161012_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselocationtime',
            name='day',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
