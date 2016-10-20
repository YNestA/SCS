# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from models import *
from tools import *
import json
# Create your views here.


def sign_in(request):
    if request.user.is_authenticated():
        logout(request)
        return render_to_response("login.html",context_instance=RequestContext(request))
    if request.method=="POST":
        try:
            username,password,user_type=request.POST.get("username",""),request.POST.get("password",""),request.POST.get("type",None)
            if user_type is None:
                render_to_response("login.html",{"login_error":"请选择登录类别"},context_instance=RequestContext(request))
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    if user.common_user_profile.if_in_group(user_type):
                        login(request,user)
                        request.session["user_type"]=user_type
                        return HttpResponseRedirect("/SCS/system/")
                    else:
                        return render_to_response("login.html",{"login_error":"用户名或密码错误"},context_instance=RequestContext(request))
                else:
                    return render_to_response("login.html",{"login_error":"账号未激活"},context_instance=RequestContext(request))
            else:
                return render_to_response("login.html",{"login_error":"用户名或密码错误"},context_instance=RequestContext(request))
        except Exception as e:
            print e
            return render_to_response("login.html",{"login_error":"系统错误"},context_instance=RequestContext(request))
    return render_to_response("login.html",context_instance=RequestContext(request))

def sign_out(request):
    if request.method=="POST":
        try:
            logout(request)
            return HttpResponse("success")
        except Exception as e:
            print e
            return HttpResponse("fail")
    return HttpResponse("You shall not pass!")

@login_required(login_url="/SCS/login/")
def system(request):
    try:
        user_type=request.session["user_type"]
    except Exception:
        return HttpResponseRedirect("/SCS/login/")
    try:
        current_term = Term.get_current_term().description
        notifies = SystemNotify.get_notifies()
        params={
                "user_type": user_type,
                "current_term": current_term,
                "notifies":[{
                    "url":"/SCS/notify"+str(notify.id),
                    "title":notify.title,
                    "time":notify.time.strftime("%Y-%m-%d %H:%M"),
                } for notify in notifies],
            }
        if user_type=="student":
            major=request.user.common_user_profile.student_profile.major
            params["dateDict"]={
                    "today":datetime.now().strftime("%Y 年 %m 月 %d 日"),
                    "start_select":major.start_select.strftime("%Y-%m-%d %H:%M"),
                    "end_select":major.end_select.strftime("%Y-%m-%d %H:%M"),
                    "start_drop":major.start_drop.strftime("%Y-%m-%d %H:%M"),
                    "end_drop":major.end_drop.strftime("%Y-%m-%d %H:%M"),
                }
        if user_type=="teacher":
            pass
        return render_to_response("system.html",params,context_instance=RequestContext(request))
    except Exception as e:
        print e
    return render_to_response("system.html",{"user_type":user_type},context_instance=RequestContext(request))

@login_required(login_url="/SCS/login/")
def look_course(request,category="all",page=1,course_name=""):
    try:
        params = {
            "user_type": request.session["user_type"],
            "categorys":[{"value":"all","description":"全部课程类别"},{"value":"nature","description":"自然科学类"},{"value":"society","description":"人文社会科学类"},{"value":"comprehensive","description":"综合类"},{"value":"art","description":"人文艺术类"}]
        }
    except Exception:
        return HttpResponseRedirect("/SCS/login")
    if request.method=="POST":
        category,course_name,page=request.POST.get("category","all"),request.POST.get("name",""),1
        params["search_input_value"],params["search_category_value"]=course_name,category

    if check_user_can_select(request.user):
        category= category_value_name[category] if category!="all" else "all"
        page,whole_page,courses=Course.get_courses(category,page,course_name=course_name)
        params["current_page"]=page
        params["all_page_num"]=range(1,whole_page+1)
        params["select_url"]="/SCS/look_course/"+category
        if courses:
            params["course_result"]=[{
                    "id":course.id,
                    "name":course.name,
                    "category":course.category.name,
                    "teacher":course.teacher.common_user_profile.name,
                    "period":course.period,
                    "credit":course.credit,
                    "amount":course.amount,
                    "capacity":course.capacity,
                } for course in courses]
        else:
            params["no_course_tip"]="未找到课程"
        if page>1: params["prev_url"]="/SCS/look_course/"+category+str(page-1)
        if page<whole_page: params["next_url"]="/SCS/look_course/"+category+str(page+1)
        return render_to_response("look_course.html",params,context_instance=RequestContext(request))
    return  render_to_response("look_course.html",{"user_type":request.session["user_type"],"no_course_tip":"不在你的选课时间内"},context_instance=RequestContext(request))

@login_required(login_url="/SCS/login/")
def select_result(request,page=1):
    try:
        select_records=SelectRecord.get_selected_course(request.user)
        params={
            "user_type":request.session["user_type"],
            "select_result":[{
            "id":record.course.id,
            "name":record.course.name,
            "category":record.course.category.name,
            "teacher":record.course.teacher.common_user_profile.name,
            "period":record.course.period,
            "credit":record.course.credit,
            "amount":record.course.amount,
            "capacity":record.course.capacity,
        } for record in select_records],
        }
    except Exception as e:
        print e
        return HttpResponseRedirect("/SCS/login/")
    return render_to_response("select_result.html",params,context_instance=RequestContext(request))

@login_required(login_url="/SCS/login/")
def finish_course(request,term_id="all",page=1,course_name=""):
    try:
        params = {
            "user_type": request.session["user_type"],
        }
    except Exception as e:
        print e
        return HttpResponseRedirect("/SCS/login/")
    if request.method=="POST":
        term_id,course_name=request.POST.get("term","all"),request.POST.get("name","")
        params["search_name"],params["search_term_id"]=course_name,int(term_id) if term_id!="all" else "all"
    term = Term.objects.get(id=term_id) if term_id != "all" else "all"
    params["terms"]=[{
                    "id":x.id,
                    "description":x.description,
                 } for x in Term.get_student_all_term(request.user)]

    page,whole_page,records=SelectRecord.get_finished_record(request.user,page,term=term,course_name=course_name)
    params["finish_course"]=[{
        "term":record.term.description,
        "name":record.course.name,
        "category":record.course.category.name,
        "teacher":record.course.teacher.common_user_profile.name,
        "period":record.course.period,
        "credit":record.course.credit,
        "score":record.score,
    } for record in records ]
    params["select_url"]="/SCS/finish_course/"+term_id+"page"
    params["all_page_num"]=range(1,whole_page+1)
    params["current_page"]=page
    if page>1:params["prev_url"]="/SCS/finish_course/"+term_id+"page"+str(page-1)
    if page<whole_page: params["next_url"]="/SCS/finish_course/"+term_id+"page"+str(page+1)
    return render_to_response("finish_course.html",params,context_instance=RequestContext(request))


def student_select_course(request):
    if request.method=="POST":
        try:
            course=Course.get_course_by_id(request.POST.get("course_id",""))
            if check_select_repeat(request.user, course):
                return HttpResponse(json.dumps({"res": "fail", "message": "repeat"}))
            if check_student_two_select(request.user):
                return HttpResponse(json.dumps({"res":"fail","message":"gt_two"}))
            if course.capacity==course.amount:
                return HttpResponse(json.dumps({"res":"fail","message":"full"}))
            if SelectRecord.create_Record(course,request.user):
                course.amount+=1
                course.save()
                return HttpResponse(json.dumps({"res":"success","amount":course.amount}))
        except Exception as e:
            print e
            return HttpResponse(json.dumps({"res":"fail"}))
    return HttpResponse("You shall not pass!")


def student_drop_course(request):
    if request.method=="POST":
        try:
            course=Course.objects.get(id=request.POST.get("course_id",""))
            if SelectRecord.drop_select_course(course,request.user):
                course.amount-=1
                course.save()
                return HttpResponse(json.dumps({"res":"success"}))
            else:
                return HttpResponse(json.dumps({"res":"fail"}))
        except Exception as e:
            print e
            return HttpResponse(json.dumps({"res":"fail"}))
    return HttpResponse("You shall not pass!")

def look_course_lt(request):
    if request.method=="POST":
        course_id=request.POST.get("course_id",None)
        if course_id:
            try:
                lts=CourseLocationTime.get_lt_by_course(Course.objects.get(id=course_id))
                return HttpResponse(json.dumps({
                    "res":"success",
                    "lts":[{
                       "week":"".join([str(lt.start_week),"-",str(lt.end_week),u"周"]),
                        "class":"".join([lt.day," ",str(lt.start_class_num),"-",str(lt.end_class_num),u"节"]),
                        "location":lt.loaction,
                        }for lt in lts],
                    }))
            except Exception as e:
                print e
                return HttpResponse(json.dumps({"res":"fail"}));
    return HttpResponse("You shall not pass!");

@login_required(login_url="/SCS/login/")
def teacher_own_course(request):
    try:
        courses=Course.own_course(request.user)
        params={
            "user_type":request.session["user_type"],
            "own_course":[{
                "id":course.id,
                "name":course.name,
                "category":course.category.name,
                "teacher":course.teacher.common_user_profile.name,
                "period":course.period,
                "credit":course.credit,
                "amount":course.amount,
                "capacity":course.capacity,
                "student_list_url":"/SCS/control_student/"+str(course.id)+"namestudentpage1",
                }for course in courses ],
        }
        return render_to_response("own_course.html", params,context_instance=RequestContext(request))
    except Exception as e:
        print e
        return HttpResponseRedirect("/SCS/login/")

@login_required(login_url="/SCS/login/")
def teacher_control_student(request,course_id="",student_id="",course_name="",page=1):
    page,per=int(page),10
    try:
        params={
            "user_type": request.session["user_type"],
        }
    except Exception as e:
        print e
        return HttpResponseRedirect("/SCS/login/")
    if request.method=="POST":
        type,value=request.POST.get("search_type",""),request.POST.get("value","")
        params["search_input_value"],params["search_type"]=value,type
        if type=="course_name":
            course_name=value
        elif type=="student_id":
            student_id=value
    courses=Course.own_course(request.user,course_name=course_name,course_id=course_id)
    students=[]
    for course in courses:
        records=course.get_select_record(student_id=student_id)
        students.extend(records)
    whole_page,page=calu_pager(students,page,per=per)
    students=students[(page-1)*per:page*per]
    for index in range(0,len(students)):
        student_profile=students[index].student.common_user_profile.student_profile
        students[index]={
                "record_id":students[index].id,
                "course_name":students[index].course.name,
                "course_category":students[index].course.category.name,
                "username":students[index].student.username,
                "name":students[index].student.common_user_profile.name,
                "college":students[index].student.common_user_profile.student_profile.college.name,
                "major":student_profile.major.name,
                "class":student_profile.grade+student_profile.s_class+u"班",
                "score":students[index].score,
            }
    params["students"]=students
    params["current_page"] = page
    params["all_page_num"] = range(1, whole_page + 1)
    params["pager_url"]="".join(["/SCS/control_student/",str(course_id),"name",course_name,"student",student_id,"page"])
    if page > 1: params["prev_url"] = "".join(["/SCS/control_student/",str(course_id),"name",course_name,"student",student_id,"page",str(page-1)])
    if page < whole_page: params["next_url"] ="".join(["/SCS/control_student/",str(course_id),"name",course_name,"student",student_id,"page",str(page+1)])

    return render_to_response("control_student.html",params,context_instance=RequestContext(request))

def modify_score(request):
    if request.method=="POST":
        try:
            req=json.loads(request.body)
            records=req["records"]
            for x in records:
                record=SelectRecord.objects.get(id=x["record_id"])
                record.modify_score(x["score"])
            return HttpResponse(json.dumps({"res":"success"}))
        except Exception as e:
            print e
            return HttpResponse(json.dumps({"res":"fail"}))
    return HttpResponse("You shall not pass!")

@login_required(login_url="/SCS/login/")
def look_notify(request,notify_id):
    try:
        params={
            "user_type":request.session["user_type"],
        }
    except Exception as e:
        print e
        return HttpResponseRedirect("/SCS/login")
    try:
        notify=SystemNotify.get_notify_by_id(notify_id)
        params["notify"]={
            "title":notify.title,
            "content":notify.content.split("\r\n"),
            "term":notify.term.description,
            "time":notify.time.strftime("%m-%d %H:%M"),
        }
        return render_to_response("notify.html",params,context_instance=RequestContext(request))
    except Exception as e:
        print e
        return render_to_response("notify.html",params,context_instance=RequestContext(request))
