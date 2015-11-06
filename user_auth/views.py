# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from . import models
from .models import Profile, Circle, PendingRequest
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
                assign_perm('add_circle', u, c_tmp)
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

def permission_request(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.user.has_perm('user_auth.change_circle'):
            if request.method == 'POST':
                username = request.POST['username']
                circle_name = request.POST['circle_name']
                user = User.objects.get(username=username)
                circle = Circle.objects.get(name=circle_name)
                user.profile.circle_set.add(circle)
                user.save()
                # # permission query没有存放,本来为view_vircle
                assign_perm('add_circle', user, circle)
                PendingRequest.objects.get(username=username, circle_name=circle_name).delete()
                messages.success(request, '成功为其赋权')
                return HttpResponseRedirect(reverse('permission_request'))
            else:
                pr = PendingRequest.objects.all()
                return render(request, 'user/pending_request.html', {'request':pr, 'messages':get_messages(request), 'user':request.user})
        else:
            messages.error(request, '您没有审核权限')
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
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
                print '原始'
                print cd['circles']
                for c in cd['circles']:
                    try:
                       cir = Circle.objects.get(name=c)
                    except:
                        messages.error(request, '请不要发送非法请求')
                        return HttpResponseRedirect(reverse('add_infomation'))

                old_cir = []
                for cir_now in request.user.profile.circle_set.all():
                    # permission query没有存放,本来为view_vircle
                    old_cir.append(cir_now.name)
                    if cir_now.name not in cd['circles']:
                        request.user.profile.circle_set.remove(cir_now)
                        remove_perm('add_circle', request.user, cir_now)
                for c_new in cd['circles']:
                    if c_new not in old_cir:
                        try:
                            cir_new = Circle.objects.get(name=c_new)
                        except:
                            messages.error(request, '请不要发送非法请求')
                        else:
                            try:
                                PendingRequest.objects.get(circle_name=c_new, username=request.user.username)
                            except:
                                p = PendingRequest(circle_name=c_new, username=request.user.username)
                                p.save()
                                messages.info(request, '已经申请加入该circle')
                            else:
                                messages.info(request, '您已发出申请,等待审核')
                            # request.user.profile.circle_set.add(cir_new)
                            # # permission query没有存放,本来为view_vircle
                            # assign_perm('add_circle', request.user, cir_new)

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
            circle_lst = []
            for c_tmp in profile.circle_set.all():
                circle_lst.append(c_tmp.name)
            tmp['circles'] = circle_lst
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