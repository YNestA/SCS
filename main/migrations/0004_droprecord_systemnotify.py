# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20161008_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('drop_time', models.DateTimeField(default=datetime.datetime.now)),
                ('course', models.ForeignKey(related_name='as_course_for_drop_record', to='main.Course')),
                ('student', models.ForeignKey(related_name='as_student_for_drop_record', to=settings.AUTH_USER_MODEL)),
                ('term', models.ForeignKey(related_name='as_term_for_drop_record', to='main.Term')),
            ],
        ),
        migrations.CreateModel(
            name='SystemNotify',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
