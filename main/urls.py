# -*- coding:utf-8 -*-
import views
from django.conf.urls import patterns,url

urlpatterns=patterns('',
    url(r'^$',views.sign_in),
    url(r'^login/',views.sign_in),
    url(r'system/',views.system),
    url(r'^sign-out/',views.sign_out),
)