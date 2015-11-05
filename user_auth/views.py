# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from . import models
from .models import Profile, Circle
from django.contrib import messages
from django.contrib.messages import get_messages
from .forms import RegisterForm, PersonalInfomations
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm, remove_perm
# Create your views here.

def site_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, '成功登录')
                return HttpResponseRedirect(reverse('site_message'))
            else:
                return HttpResponseRedirect(reverse('index_not_login'))
        else:
            messages.error(request, '登录失败,请检查您的用户名和密码是否正确')
            return HttpResponseRedirect(reverse('index_not_login'))
    else:
        return HttpResponseRedirect(reverse('index_not_login'))


def site_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']):
                messages.error(request, '账号已被注册')
            else:
                u = User.objects.create_user(username=cd['username'],password=cd['password'])
                u.save()
                u_profile = Profile(user = u)
                c_tmp = Circle.objects.get(name='public')
                u_profile.save()
                u_profile.circle_set.add(c_tmp)
                u_profile.save()
                u = authenticate(username=cd['username'], password=cd['password'])
                # User.objects.create_user(username=cd['username'], password=cd['password'])
                login(request, u)
                messages.success(request, '注册成功,您已登录')
        else:
            messages.error(request, '请正确填写表单')

        return HttpResponseRedirect(reverse('index_not_login'))
    else:
        return HttpResponseRedirect(reverse('index_not_login'))


def add_infomation(request):
    if request.user.is_authenticated() and request.user.is_active:
        u_registered = User.objects.get(username=request.user.username)
        if request.method == 'POST':
            form = PersonalInfomations(request.POST)
            circleselectchoice = []
            c_all = Circle.objects.all()
            for c in c_all:
                circleselectchoice.append((c.name,c.name))
            form.fields['circles'].__init__(choices=circleselectchoice)
            if form.is_valid():
                cd = form.cleaned_data
                profile = request.user.profile
                profile.nickname = cd['nickname']
                profile.birthday = cd['birthday']
                profile.grade = cd['grade']
                profile.phone_number = cd['phone_number']
                profile.school = cd['school']
                profile.school_id = cd['school_id']
                profile.sex = cd['sex']
                request.user.email = cd['email']
                request.user.first_name = cd['name']
                for c in cd['circles']:
                    try:
                       cir = Circle.objects.get(name=c)
                    except:
                        messages.error(request, '请不要发送非法请求')
                        return HttpResponseRedirect(reverse('add_infomation'))
                request.user.profile.circle_set.clear()
                for cir_now in request.user.profile.circle_set.all():
                    remove_perm('view_circle', request.user, cir_now)
                for c in cd['circles']:
                    try:
                        cir = Circle.objects.get(name=c)
                    except:
                        messages.error(request, '请不要发送非法请求')
                    else:
                        request.user.profile.circle_set.add(cir)
                        assign_perm('view_circle', request.user, cir)

                request.user.profile.save()
                request.user.save()
                profile.save()

                messages.success(request, '您已经成功更新个人资料')
                return HttpResponseRedirect(reverse('site_message'))
        else:
            profile = request.user.profile
            tmp = {}
            tmp['nickname'] = profile.nickname
            tmp['birthday'] = profile.birthday
            tmp['grade'] = profile.grade
            tmp['phone_number'] = profile.phone_number
            tmp['school'] = profile.school
            tmp['school_id'] = profile.school_id
            tmp['sex'] = profile.sex
            tmp['email'] = request.user.email
            tmp['name'] = request.user.first_name

            form = PersonalInfomations(initial=tmp)
            circleselectchoice = []
            c_all = Circle.objects.all()
            for c in c_all:
                circleselectchoice.append((c.name,c.name))
            form.fields['circles'].__init__(choices=circleselectchoice)

        return render(request, 'user/add_infomation.html', {'form':form, 'message':get_messages(request), 'user':request.user})

    else:
        messages.error(request, '您的账户没有权限')
        return HttpResponseRedirect(reverse('index_not_login'))


def site_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index_not_login'))