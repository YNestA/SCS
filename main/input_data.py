# -*- coding:utf-8 -*-
from random import *
from django.contrib.auth.models import *
from models import *

'''此为测试文件'''

students_first_name=["柁","古","范","芈","李","吴","时","慕容","乔","西门"]
students_last_name=["嘉熹","廷钰","日天","复","铁柱","越","峰","吹雪","钦诚","一一"]
teachers_first_name=["向","张","丁","王","刁","苏","段","孔","杨"]
teachers_last_name=["问","成","无","升","霖","帅","二","三","延","过"]
colleges=College.objects.all()
majors=Major.objects.all()
grades=["2014","2015","2016"]
s_classes=["01","02","03"]
professionals=["讲师","副教授","教授"]

def set_students_name():
    students=Group.objects.get(name="student").user_set.all()
    names=[]
    for x in students:
        name=students_first_name[randint(0,9)]+students_last_name[randint(0,9)]
        while name in names:
            name = students_first_name[randint(0, 9)] + students_last_name[randint(0, 9)]
        names.append(name)
        x.common_user_profile.name=name
        x.common_user_profile.TEL=''.join([ str(randint(0,9)) for count in xrange(0,11)])
        x.common_user_profile.save()
        college=colleges[randint(0,len(colleges)-1)]
        major=college.majors.all()[randint(0,len(college.majors.all())-1)]
        student_profile=StudentProfile(common_profile=x.common_user_profile,college=college,major=major,grade=grades[randint(0,2)],s_class=s_classes[randint(0,2)])
        student_profile.save()
def look_students_name():
    students = Group.objects.get(name="student").user_set.all()
    for x in students:
        print x.common_user_profile.name

def set_teachers_name():
    teachers=Group.objects.get(name="teacher").user_set.all()
    names=[]
    for x in teachers:
        name=teachers_first_name[randint(0,8)]+teachers_last_name[randint(0,8)]
        while name in names:
            name = teachers_first_name[randint(0, 8)] + teachers_last_name[randint(0, 8)]
        names.append(name)
        x.common_user_profile.name=name
        x.common_user_profile.TEL=''.join([ str(randint(0,9)) for count in xrange(0,11)])
        x.common_user_profile.save()
        teacher_profile=TeacherProfile(common_profile=x.common_user_profile,college=colleges[randint(0,len(colleges)-1)],professional_title=professionals[randint(0,2)])
        teacher_profile.save()

def students_select_course():
    students=Group.objects.get(name="student").user_set.all()
    courses=Course.objects.all()
    for stu in students:
        index1=randint(0,len(courses)-1)
        index2=randint(0,len(courses)-1)
        while index1==index2:
            index2=randint(0,len(courses)-1)
        SelectRecord.create_Record(courses[index1],stu)
        SelectRecord.create_Record(courses[index2],stu)
        courses[index1].amount+=1
        courses[index2].amount += 1
        courses[index1].save()
        courses[index2].save()

def set_courses_lt():
    courses=Course.objects.all()
    for course in courses:
        lt=CourseLocationTime(start_week=2,end_week=11,start_class_num=9,end_class_num=11,loaction="东十二 110",term=Term.get_current_term(),day="周三",course=course)
        lt.save()