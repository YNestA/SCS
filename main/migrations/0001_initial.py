# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
                ('dean', models.ForeignKey(related_name='as_dean_for_college', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommonUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('sex', models.CharField(max_length=10)),
                ('head_img', models.CharField(default=b'/static/image/', max_length=500)),
                ('TEL', models.CharField(max_length=20)),
                ('user', models.OneToOneField(related_name='common_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('capacity', models.IntegerField()),
                ('amount', models.IntegerField(default=0)),
                ('period', models.IntegerField()),
                ('credit', models.IntegerField()),
                ('can_selected', models.BooleanField(default=True)),
                ('category', models.ForeignKey(related_name='as_category_for_course', to='main.Category')),
            ],
        ),
        migrations.CreateModel(
            name='CourseLocationTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_week', models.IntegerField()),
                ('end_week', models.IntegerField()),
                ('start_class_num', models.IntegerField()),
                ('end_class_num', models.IntegerField()),
                ('loaction', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('start_select', models.DateTimeField(blank=True)),
                ('end_select', models.DateTimeField(blank=True)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='SelectRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('select_time', models.DateTimeField(default=datetime.datetime.now)),
                ('course', models.ForeignKey(related_name='as_course_for_select_record', to='main.Course')),
                ('student', models.ForeignKey(related_name='as_student_for_select_record', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.CharField(max_length=100)),
                ('s_class', models.CharField(max_length=100)),
                ('college', models.ForeignKey(related_name='as_college_for_student_profile', to='main.College')),
                ('common_profile', models.OneToOneField(related_name='student_profile', to='main.CommonUserProfile')),
                ('major', models.ForeignKey(related_name='as_major_for_student_profile', to='main.Major')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('professional_title', models.CharField(max_length=100)),
                ('college', models.ForeignKey(related_name='as_college_for_teacher_profile', to='main.College')),
                ('common_profile', models.OneToOneField(related_name='teacher_profile', to='main.CommonUserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=500)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='selectrecord',
            name='term',
            field=models.ForeignKey(related_name='as_term_for_select_record', to='main.Term'),
        ),
        migrations.AddField(
            model_name='courselocationtime',
            name='term',
            field=models.ForeignKey(to='main.Term'),
        ),
        migrations.AddField(
            model_name='course',
            name='location_time',
            field=models.ManyToManyField(related_name='as_lt_for_course', to='main.CourseLocationTime'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(related_name='as_teacher_for_course', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='college',
            name='majors',
            field=models.ManyToManyField(related_name='as_major_for_college', to='main.Major'),
        ),
    ]
