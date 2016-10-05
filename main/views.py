# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def sign_in(request):
    if request.user.is_authenticated():
        logout(request)
        return render_to_response("login.html",context_instance=RequestContext(request))
    if request.method=="POST":
        try:
            username,password=request.POST.get("username",""),request.POST.get("password","")
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/SCS/system/")
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
    return render_to_response("system.html",context_instance=RequestContext(request))