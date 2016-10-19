# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_systemnotify_term'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='droprecord',
            name='course',
        ),
        migrations.RemoveField(
            model_name='droprecord',
            name='student',
        ),
        migrations.RemoveField(
            model_name='droprecord',
            name='term',
        ),
        migrations.AddField(
            model_name='selectrecord',
            name='if_drop',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='DropRecord',
        ),
    ]
