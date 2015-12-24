# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from . import models
from content.models import Follow, FollowSensor
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
                if cd['password'] != cd['password_reconfirm']:
                    messages.error(request, '两次输入密码不符')
                else:
                    u = User.objects.create_user(username=cd['username'],password=cd['password'])
                    permission = Permission.objects.get(codename='open_relationship')
                    u.user_permissions.add(permission)
                    u.save()
                    u_profile = Profile(user = u)
                    c_tmp = Circle.objects.get(name='public')
                    u_profile.save()
                    u_profile.circle_set.add(c_tmp)

                    assign_perm('add_circle', u, c_tmp)
                    u_profile.save()
                    u_auth = authenticate(username=cd['username'], password=cd['password'])
                    # User.objects.create_user(username=cd['username'], password=cd['password'])
                    login(request, u_auth)
                    messages.success(request, '注册成功,您已登录')
                    f = Follow()
                    f.follower = u.id
                    f.followed = u.id
                    f.save()
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


def search_to_follow(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            profile_lst = Profile.objects.filter(nickname__contains =request.POST.get('name', -1))
            return render(request, 'user/search_to_follow.html', {'profile_lst':profile_lst, 'messages':get_messages(request), 'user':request.user})
        else:
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def add_follow(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            try:
                usr = User.objects.get(id=int(request.POST['user_id']))

            except:
                messages.error(request, '请不要非法修改数据')
                return HttpResponseRedirect(reverse('search_to_follow'))

            if usr.has_perm('user_auth.open_relationship'):
                if Follow.objects.filter(follower=request.user.id, followed=usr.id):
                    messages.warning(request, '您已经添加过这名好友了')
                else:
                    f = Follow()
                    f.follower = request.user.id
                    f.followed = usr.id
                    f.save()

                    if request.user.profile.follow_count:
                        request.user.profile.follow_count += 1
                    else:
                        request.user.profile.follow_count = 1
                    request.user.profile.save()

                    if usr.profile.followed_count:
                        usr.profile.followed_count += 1
                    else:
                        usr.profile.followed_count = 1
                    usr.profile.save()
                    messages.success(request, '申请成功')
            elif usr.has_perm('user_auth.censor_relationship'):
                if FollowSensor.objects.filter(whoto=request.user.id, censor=usr.id):
                    messages.info(request, '请耐心等待对方审核')
                else:
                    if Follow.objects.filter(follower=request.user.id, followed=usr.id):
                        messages.warning(request, '您已经添加过这名好友了')
                    else:
                        f_censor = FollowSensor()
                        f_censor.whoto = request.user.id
                        f_censor.censor = usr.id
                        f_censor.save()
                        if usr.profile.censor_count:
                            usr.profile.censor_count += 1
                        else:
                            usr.profile.censor_count = 1
                        usr.profile.save()
                        messages.info(request, '您已经成功发出请求')
            else:
                messages.error(request, '您申请关注的用户不允许被关注')

            return HttpResponseRedirect(reverse('search_to_follow'))
        else:
            return HttpResponseRedirect(reverse('search_to_follow'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def censor_follow(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            allow_id = request.POST.get('allow_id', -1)
            if allow_id >= 0:
                if Follow.objects.filter(follower=int(allow_id), followed=request.user.id):
                    messages.warning(request, '您已经添加过这名好友了')
                else:
                    f = Follow()
                    f.follower = int(allow_id)
                    f.followed = request.user.id
                    f.save()

                    allow_usr = User.objects.get(id=int(allow_id))
                    if allow_usr.profile.follow_count:
                        allow_usr.profile.follow_count += 1
                    else:
                        allow_usr.profile.follow_count = 1
                    allow_usr.profile.save()

                    if request.user.profile.followed_count:
                        request.user.profile.followed_count += 1
                    else:
                        request.user.profile.followed_count = 1
                    request.user.profile.save()
                    
                    messages.success(request, '您已成功同意申请')


                    request.user.profile.censor_count -= 1
                    request.user.profile.save()
                    f_censor = FollowSensor.objects.get(whoto=int(allow_id), censor=request.user.id).delete()
            else:
                messages.error(request, '请不要发送非法请求')
            return HttpResponseRedirect(reverse('censor_follow'))
        else:
            censor_id = request.user.id
            who_to_censor = FollowSensor.objects.filter(censor=censor_id)
            profile_lst = []
            for i in who_to_censor:
                u = User.objects.get(id=i.whoto)
                profile_lst.append(u.profile)
            return render(request, 'user/censor_list.html', {'censor_lst':who_to_censor,'profile_lst':profile_lst, 'messages':get_messages(request), 'user':request.user})
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def reject_follow(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            whoto = request.POST.get('allow_id', -1)
            censor = request.POST.get('my_id', -1)
            FollowSensor.objects.get(whoto=whoto, censor=censor).delete()
            request.user.profile.censor_count -= 1
            request.user.profile.save()
        return HttpResponseRedirect(reverse("censor_follow"))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))


def delete_follow(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            delete_id = request.POST.get('user_id', -1)
            if delete_id > 0:
                Follow.objects.get(follower=request.user.id, followed=int(delete_id)).delete()
                if request.user.profile.follow_count:
                    request.user.profile.follow_count -= 1
                    request.user.profile.save()

                delete_usr = User.objects.get(id=int(delete_id))
                if delete_usr.profile.followed_count:
                    delete_usr.profile.followed_count -= 1
                    delete_usr.profile.save()
            messages.success(request, '您已成功删除')
            return HttpResponseRedirect(reverse('view_follower', args=(request.user.id,)))
        else:
            return HttpResponseRedirect(reverse('view_follower', args=(request.user.id,)))
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
                auth_status = cd['follow_auth']

                # process follow_auth

                # get permmision
                p_free = Permission.objects.get(codename='open_relationship')
                p_censor = Permission.objects.get(codename='censor_relationship')
                # clear the permission
                try:
                    request.user.user_permissions.remove(p_free)
                except:
                    pass
                try:
                    request.user.user_permissions.remove(p_censor)
                except:
                    pass

                if auth_status == 'free':
                    request.user.user_permissions.add(p_free)
                elif auth_status == 'censor':
                    request.user.user_permissions.add(p_censor)

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
            if request.user.has_perm('user_auth.open_relationship'):
                tmp['follow_auth'] = 'free'
            elif request.user.has_perm('user_auth.censor_relationship'):
                tmp['follow_auth'] = 'censor'
            else:
                tmp['follow_auth'] = 'forbidden'
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