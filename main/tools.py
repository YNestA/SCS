# -*- coding:utf-8 -*-
from datetime import datetime
from models import *

MAX_PER_CAN_SELECT=2

category_value_name={
    "all":"全部课程类别",
    "nature":"自然科学类",
    "society":"人文社会科学类",
    "comprehensive":"综合类",
    "art":"人文艺术类",
}

def check_user_can_select(user):
    major=user.common_user_profile.student_profile.major
    return datetime.now()>major.start_select and datetime.now()<major.end_select

def check_select_repeat(user,course):
    return SelectRecord.objects.filter(student=user,course=course,term=Term.get_current_term(),if_drop=False)

def check_student_two_select(user):
    return len(SelectRecord.objects.filter(student=user,term=Term.get_current_term(),if_drop=False))>=MAX_PER_CAN_SELECT

def calu_pager(students,page,per=1):
    whole_page=len(students)/per+1 if len(students)%per!=0 else len(students)/per
    if page>whole_page:page=whole_page
    if page<1:page=1
    return (whole_page,page)