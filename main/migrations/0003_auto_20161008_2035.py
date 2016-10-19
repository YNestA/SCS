# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20161004_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='end_drop',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='major',
            name='start_drop',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='major',
            name='end_select',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='major',
            name='start_select',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
