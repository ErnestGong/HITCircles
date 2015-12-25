# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from user_auth.models import Profile
from content.models import Follow, Content
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
import datetime
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages import get_messages
from user_auth.forms import LoginForm, RegisterForm, AddContent, Circle
from .models import Web, Web1
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group


def scrapy_show(request):
    if request.user.is_authenticated() and request.user.is_active:
        details1 = Web.objects.all()
        details2 = Web1.objects.all()
        detail1 = []
        detail2 = []
        len1 = len(details1)
        len2 = len(details2)
        if len1 <= 0 and len2 <= 0:
            return render(request, 'scrapy_show.html',{"message":"No information"})
        for i in range (0,len1):
            details1[i].content = details1[i].content.replace("/uploadfiles","http://today.hit.edu.cn/uploadfiles")
            detail1.append(details1[i])
        for i in range(0,len2):
            details2[i].content1 = details2[i].content1.replace("/uploadfiles","http://today.hit.edu.cn/uploadfiles")
            detail2.append(details2[i])
        detail1.sort(reverse = True,cmp=lambda x,y:cmp(x.link,y.link))
        detail2.sort(reverse = True,cmp=lambda x,y:cmp(x.link1,y.link1))
        return render(request, 'scrapy_show.html',{"messages1":detail1,"messages2":detail2})
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def return_404(request):
    return render(request, 'user/404.html', {'user':request.user})
    
def index_not_login(request):
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect(reverse('site_message'))
    else:
        form = LoginForm()
        form1 = RegisterForm()
        return render(request, 'user/index_not_login.html', {'messages':get_messages(request), 'form':form, 'form1':form1, 'user':request.user})


def site_message(request):
    # 不考虑用post的情况下,引入权限设置
    if request.user.is_authenticated() and request.user.is_active:
        if request.user.profile.nickname is not None:
            top_lst_ten = []
            try:
                circle = request.user.profile.circle_set.all()
            except:
                messages.error(request, '请不要发出非法请求')
                return HttpResponseRedirect(reverse('site_message'))
            else:
                content = []
                for c in circle:
                    if c.name == 'public':
                        tmp = []
                        for follow_usr_lst in Follow.objects.filter(follower=request.user.id):
                            u = User.objects.get(id=follow_usr_lst.followed)
                            p = u.profile
                            sort_tmp = []
                            p_content = p.content_set.all().filter(circles__name='public')
                            if p_content:
                                for sort_count in p_content:
                                    sort_tmp.append(sort_count)
                                if sort_tmp:
                                    sort_tmp.reverse()
                                    tmp += sort_tmp[:]
                            else:
                                tmp += []


                    else:
                        tmp = c.content_set.all()
                        sort_tmp = []
                        if tmp:
                            for sort_count in tmp:
                                sort_tmp.append(sort_count)
                            if sort_tmp:
                                tmp = sort_tmp.reverse()[:]
                    result = []
                    for t_counter in tmp:
                        if request.user.has_perm('added_thumb_up', t_counter):
                            result.append([c.name, t_counter, 1])
                        else:
                            result.append([c.name, t_counter, 0])
                    if not result:
                        result.append([c.name, ''])
                    content.append(result)
                    top_lst = Content.objects.filter(circles__name='public').order_by('-thumb_up')
                    top_lst_ten = []
                    top_lst_count = 0
                    for top_lst_tmp in top_lst:
                        if top_lst_count >= 10:
                            break
                        top_lst_ten.append(top_lst_tmp)
                        top_lst_count += 1

            if request.method == 'POST':
                form = AddContent(request.POST)
                circle_user_choice = []
                c_all = request.user.profile.circle_set.all()
                for c in c_all:

                    circle_user_choice.append((c.name,c.name))
                form.fields['circle'].__init__(choices=circle_user_choice)
                if form.is_valid():
                    cd = form.cleaned_data
                    author = request.user.username
                    title = cd['title']
                    content = cd['content']
                    c = request.user.profile.content_set.create(title=title, text=content, thumb_up=0)


                    try:
                        my_circle = Circle.objects.get(name = cd['circle'])

                        # print c_info
                    except:
                        messages.error(request, '请不要非法修改信息')
                    else:
                        c.circles.add(my_circle)
                        c.save()
                        assign_perm('delete_content', request.user, c)
                        messages.success(request, '成功添加内容')
                    return HttpResponseRedirect(reverse('site_message'))
                return render(request, 'user/message.html', {'circle':circle, 'top_ten':top_lst_ten, 'content':content, 'form':form, 'user':request.user, 'messages':get_messages(request)})

            else:
                form = AddContent()
                circle_user_choice = []
                c_all = request.user.profile.circle_set.all()
                for c in c_all:

                    circle_user_choice.append((c.name,c.name))
                form.fields['circle'].__init__(choices=circle_user_choice)
                return render(request, 'user/message.html', {'circle':circle,'top_ten':top_lst_ten, 'content':content, 'form':form, 'user':request.user, 'messages':get_messages(request)})
        else:
            return HttpResponseRedirect(reverse('add_infomation'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))
