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
                Content.objects.get(id=content_id).delete()
                messages.success(request, '成功删除该条信息')
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
        if profile_id:
            try:
                p = Profile.objects.get(id=profile_id)
            except:
                messages.error('请不要发出非法请求')
                return HttpResponseRedirect(reverse('site_message'))
            else:
                content = p.content_set.all()
                return render(request, 'content/my_mainpage.html', {'content':content, 'profile':p})
        else:
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
                messages.error('请不要发出非法请求')
                return HttpResponseRedirect(reverse('site_message'))
            else:
                content = c.content_set.all()
                return render(request, 'content/circle.html', {'content':content, 'circle': c})
        else:
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))