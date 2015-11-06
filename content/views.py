# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Content
from user_auth.models import Circle, Profile
from user_auth.forms import AddContent
# Create your views here

def delete_content(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            content_id = request.POST.get('delete_id')
            try:
                content_id = int(content_id)
                cont = Content.objects.get(id=content_id)
                if request.user.has_perm('delete_content', cont):
                    cont.delete()
                    messages.success(request, '成功删除该条信息')
                else:
                    messages.error(request, '您没有删除权限')
            except:
                messages.error(request, '请不要发出非法请求')

            return HttpResponseRedirect(reverse('site_message'))
        else:
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def view_content_profile(request, profile_id):
    # 不考虑用post的情况下,引入权限设置
    if request.user.is_authenticated() and request.user.is_active:
        if profile_id and int(profile_id) == request.user.profile.id:
            try:
                p = Profile.objects.get(id=profile_id)
            except:
                messages.error(request, '请不要发出非法请求')
                return HttpResponseRedirect(reverse('site_message'))
            else:
                content = p.content_set.all()
                return render(request, 'content/my_mainpage.html', {'content':content, 'profile':p, 'user':request.user, 'messages':get_messages(request)})
        else:
            messages.error(request, '请查看本人的资料')
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def view_content_circle(request, circle_id):
    # 不考虑用post的情况下,引入权限设置
    if request.user.is_authenticated() and request.user.is_active:
        if circle_id:
            try:
                c = Circle.objects.get(id=circle_id)
            except:
                messages.error(request, '请不要发出非法请求')
                return HttpResponseRedirect(reverse('site_message'))
            else:
                # permission query没有存放,本来为view_vircle
                if request.user.has_perm('add_circle', c):
                    content = c.content_set.all()
                    return render(request, 'content/circle.html', {'content':content, 'circle': c, 'user':request.user, 'messages':get_messages(request)})
                else:
                    messages.error(request, '您没有权限查看这个circle的资料')
                    return HttpResponseRedirect(reverse('site_message'))
        else:
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))