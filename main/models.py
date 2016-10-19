# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models.signals import post_save
from datetime import datetime
import re
# Create your models here.

class Major(models.Model):
    name=models.CharField(max_length=500)
    start_select=models.DateTimeField(blank=True,null=True)
    end_select=models.DateTimeField(blank=True,null=True)
    start_drop=models.DateTimeField(blank=True,null=True)
    end_drop=models.DateTimeField(blank=True,null=True)
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

    @staticmethod
    def get_current_term():
        current_time=datetime.now()
        return Term.objects.filter(start_date__lt=current_time,end_date__gt=current_time)[0]

    @staticmethod
    def get_student_all_term(student):
        try:
            the_grade=int(student.common_user_profile.student_profile.grade)
            first_term=Term.objects.filter(start_date__gte=datetime(the_grade,1,1),start_date__lt=datetime(the_grade+1,1,1))[1]
            return Term.objects.filter(start_date__gte=first_term.start_date,start_date__lte=Term.get_current_term().start_date).order_by("start_date")[:7]
        except Exception as e:
            print e
            return None
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

    @staticmethod
    def get_courses(category,page,course_name="",per=10):
        page=int(page)
        if category!="all":
            courses=Course.objects.filter(category=Category.objects.get(name=category),name__contains=course_name,can_selected=True)
        else:
            courses=Course.objects.filter(name__contains=course_name,can_selected=True)
        whole_page=len(courses)/per+1 if len(courses)%per!=0 else len(courses)/per
        if page > whole_page:
            print "="
            page=whole_page
        if page<1:page=1
        print page,whole_page
        return (page,whole_page,courses[per*(page-1):per*page])

    @staticmethod
    def get_course_by_id(course_id):
        return Course.objects.get(id=course_id)


    @staticmethod
    def own_course(teacher,course_name="",course_id=""):
        if str(course_id):
            return Course.objects.filter(teacher=teacher,can_selected=True,name__contains=course_name,id=int(course_id))
        else:
            return Course.objects.filter(teacher=teacher, can_selected=True, name__contains=course_name)

    def get_select_record(self,student_id=""):
        def __filter(x):
            return str(x.student.username).find(student_id)!=-1
        return filter(__filter,SelectRecord.objects.filter(course=self,term=Term.get_current_term(),if_drop=False))

    def __unicode__(self):
        return self.name

class CourseLocationTime(models.Model):
    start_week=models.IntegerField()
    end_week=models.IntegerField()
    start_class_num=models.IntegerField()
    end_class_num=models.IntegerField()
    loaction=models.CharField(max_length=100)
    term=models.ForeignKey(Term)
    day=models.CharField(max_length=20)
    course=models.ForeignKey(Course,related_name="as_course_for_lt",null=True)

    @staticmethod
    def get_lt_by_course(course,term=Term.get_current_term()):
        return CourseLocationTime.objects.filter(course=course,term=term)
    def __unicode__(self):
        return ' | '.join([self.course.name,str(self.start_week)+'-'+str(self.end_week),str(self.start_class_num)+'-'+str(self.end_class_num)])


class SelectRecord(models.Model):
    student=models.ForeignKey(User,related_name="as_student_for_select_record")
    course=models.ForeignKey(Course,related_name="as_course_for_select_record")
    term=models.ForeignKey(Term,related_name="as_term_for_select_record")
    select_time=models.DateTimeField(default=datetime.now)
    if_drop=models.BooleanField(default=False)
    score=models.CharField(max_length=10,default="",blank=True)

    @staticmethod
    def create_Record(course,student):
        record=SelectRecord(student=student,course=course,term=Term.get_current_term())
        record.save()
        return True

    @staticmethod
    def get_selected_course(student,term=Term.get_current_term()):
        return SelectRecord.objects.filter(student=student,term=term,if_drop=False)

    def __unicode__(self):
        return ' | '.join([self.course.name,self.student.username,self.term.description])

    @staticmethod
    def drop_select_course(course,student):
        try:
            the_record=SelectRecord.objects.get(student=student,course=course,term=Term.get_current_term(),if_drop=False,score="")
            the_record.if_drop=True
            the_record.save()
            return True
        except Exception as e:
            print e
            return False

    @staticmethod
    def get_finished_record(student,page,term="all",course_name="",course_id="",per=10):
        page=int(page)
        try:
            courses = Course.objects.filter(id=course_id,name__contains=course_name) if str(course_id) else Course.objects.filter(name__contains=course_name)
            if term=="all":
                records=SelectRecord.objects.filter(student=student,if_drop=False,course__in=courses).exclude(score="")
            else:
                records=SelectRecord.objects.filter(student=student,if_drop=False,term=term,course__in=courses).exclude(score="")
            whole_page = len(records) / per + 1 if len(records) % per != 0 else len(records) / per
            if page > whole_page: page = whole_page
            if page < 1: page = 1
            return (page, whole_page, records[per * (page - 1):per * page])
        except Exception as e:
            print e
            return None

    def modify_score(self,score):
        if re.match(r"^\d+(\.\d+){0,1}$",score):
            self.score=score
            self.save()

'''
class DropRecord(models.Model):
    student=models.ForeignKey(User,related_name="as_student_for_drop_record")
    course=models.ForeignKey(Course,related_name="as_course_for_drop_record")
    term=models.ForeignKey(Term,related_name="as_term_for_drop_record")
    drop_time=models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return ' | '.join([self.course.name,self.student.username,self.term.description])
'''

class SystemNotify(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    term=models.ForeignKey(Term,related_name="as_term_for_notify",null=True)
    time=models.DateTimeField(default=datetime.now)

    @staticmethod
    def get_notifies(term=Term.get_current_term()):
        return SystemNotify.objects.filter(term=term).order_by("-time")

    @staticmethod
    def get_notify_by_id(notify_id):
        return SystemNotify.objects.get(id=notify_id)
    def __unicode__(self):
        return ' | '.join([self.title,self.content])

class CommonUserProfile(models.Model):
    user=models.OneToOneField(User,related_name="common_user_profile")
    name=models.CharField(max_length=500)
    sex=models.CharField(max_length=10)
    head_img=models.CharField(max_length=500,default="/static/image/")
    TEL=models.CharField(max_length=20)

    def if_in_group(self,group_name):
        return self.user.groups.filter(name=group_name)
    def __unicode__(self):
        return  ' | '.join([self.name,self.user.username])

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