# -*- coding:utf-8 -*-
import views
from django.conf.urls import patterns,url

urlpatterns=patterns('',
    url(r'^$',views.sign_in),
    url(r'^login/$',views.sign_in),
    url(r'^system/$',views.system),
    url(r'^sign_out/$',views.sign_out),
    url(r'^look_course/$',views.look_course,{"category":"all","page":"1"}),
    url(r'^look_course/search/$',views.look_course),
    url(r'^look_course/(?P<category>[a-z]+)(?P<page>\d+)/$',views.look_course),
    url(r'^select_result(?P<page>\d*)/$',views.select_result),
    url(r'^finish_course/$',views.finish_course,{"term_id":"all","page":"1"}),
    url(r'^finish_course/search/$', views.finish_course,),
    url(r'^finish_course/(?P<term_id>\d+|all)page(?P<page>\d+)/$',views.finish_course),
    url(r'^student_select_course/$',views.student_select_course),
    url(r'^student_drop_course/$',views.student_drop_course),
    url(r'^look_course_lt/$',views.look_course_lt),
    url(r'^own_course/$',views.teacher_own_course),
    url(r'^control_student/$',views.teacher_control_student,{"course_id":"","student_id":"","course_name":"","page":"1"}),
    url(r'^control_student/search/$',views.teacher_control_student),
    url(r'^control_student/(?P<course_id>\d*)name(?P<course_name>.*)student(?P<student_id>.*)page(?P<page>\d+)/$',views.teacher_control_student),
    url(r'^modify_score/$',views.modify_score),
    url(r'^notify(?P<notify_id>\d+)/$',views.look_notify),
)