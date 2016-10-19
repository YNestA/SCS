# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_selectrecord_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemnotify',
            name='term',
            field=models.ForeignKey(related_name='as_term_for_notify', to='main.Term', null=True),
        ),
    ]
