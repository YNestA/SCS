# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime
# Create your models here.

class Major(models.Model):
    name=models.CharField(max_length=500)
    start_select=models.DateTimeField(blank=True)
    end_select=models.DateTimeField(blank=True)
    create_time=models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

class College(models.Model):
    name=models.CharField(max_length=500)
    dean=models.ForeignKey(User,related_name="as_dean_for_college",blank=True)
    majors=models.ManyToManyField(Major,related_name="as_major_for_college",blank=True)
    create_time=models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name=models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Term(models.Model):
    description=models.CharField(max_length=500)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()

    def __unicode__(self):
        return self.description



class Course(models.Model):
    name=models.CharField(max_length=500)
    teacher=models.ForeignKey(User,related_name="as_teacher_for_course")
    category=models.ForeignKey(Category,related_name="as_category_for_course")
    capacity=models.IntegerField()
    amount=models.IntegerField(default=0)
    period=models.IntegerField()
    credit=models.IntegerField()
    can_selected=models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class CourseLocationTime(models.Model):
    start_week=models.IntegerField()
    end_week=models.IntegerField()
    start_class_num=models.IntegerField()
    end_class_num=models.IntegerField()
    loaction=models.CharField(max_length=100)
    term=models.ForeignKey(Term)
    course=models.ForeignKey(Course,related_name="as_course_for_lt",null=True)

    def __unicode__(self):
        return ' | '.join([self.course.name,str(self.start_week)+'-'+str(self.end_week),str(self.start_class_num)+'-'+str(self.end_class_num)])


class SelectRecord(models.Model):
    student=models.ForeignKey(User,related_name="as_student_for_select_record")
    course=models.ForeignKey(Course,related_name="as_course_for_select_record")
    term=models.ForeignKey(Term,related_name="as_term_for_select_record")
    select_time=models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return '|'.join([self.course.name,self.student.username,self.term.description])

class CommonUserProfile(models.Model):
    user=models.OneToOneField(User,related_name="common_user_profile")
    name=models.CharField(max_length=500)
    sex=models.CharField(max_length=10)
    head_img=models.CharField(max_length=500,default="/static/image/")
    TEL=models.CharField(max_length=20)

    def __unicode__(self):
        return  self.user.username

def create_user_profile(sender,instance,created,**kw):
    if created:
        CommonUserProfile.objects.create(user=instance)

post_save.connect(create_user_profile,sender=User)

class TeacherProfile(models.Model):
    common_profile=models.OneToOneField(CommonUserProfile,related_name='teacher_profile')
    college=models.ForeignKey(College,related_name="as_college_for_teacher_profile")
    professional_title=models.CharField(max_length=100)

    def __unicode__(self):
        return self.common_profile.name+' | '+self.college.name

class StudentProfile(models.Model):
    common_profile=models.OneToOneField(CommonUserProfile,related_name='student_profile')
    college=models.ForeignKey(College,related_name="as_college_for_student_profile")
    major=models.ForeignKey(Major,related_name="as_major_for_student_profile")
    grade=models.CharField(max_length=100)
    s_class=models.CharField(max_length=100)

    def __unicode__(self):
        return ' | '.join([self.common_profile.name,self.college.name,self.major.name,self.grade,self.s_class])