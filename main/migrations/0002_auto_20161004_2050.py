# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='location_time',
        ),
        migrations.AddField(
            model_name='courselocationtime',
            name='course',
            field=models.ForeignKey(related_name='as_course_for_lt', to='main.Course', null=True),
        ),
        migrations.AlterField(
            model_name='college',
            name='dean',
            field=models.ForeignKey(related_name='as_dean_for_college', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='college',
            name='majors',
            field=models.ManyToManyField(related_name='as_major_for_college', to='main.Major', blank=True),
        ),
    ]
