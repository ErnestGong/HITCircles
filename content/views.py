# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from guardian.shortcuts import assign_perm, remove_perm
from .models import Content, Follow, Comment
from user_auth.models import Circle, Profile
from user_auth.forms import AddContent
from django.contrib.auth.models import User
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

def add_comment(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            cont_id = request.POST.get('cont_id')
            comment = request.POST.get('comment')
            user_id = request.POST.get('user_id')
            if comment and cont_id and user_id:
                u = User.objects.get(id=int(user_id))
                c_add = Content.objects.get(id=int(cont_id)).comment_set.create(text=comment, profile=u.profile)
                messages.success(request, '成功添加评论')
                c_comment = Content.objects.get(id=int(cont_id)).comment_set.all()
                c_reverse = []
                for reverse_count in c_comment:
                    c_reverse.append(reverse_count)
                c_reverse.reverse()
                c_comment = c_reverse[:]
                return render(request, 'content/add_comment.html', {'cont_id':cont_id, 'c_comment':c_comment, 'user':request.user, 'messages':get_messages(request)})
            elif cont_id:
                c_comment =  Content.objects.get(id=int(cont_id)).comment_set.all()
                c_reverse = []
                for reverse_count in c_comment:
                    c_reverse.append(reverse_count)
                c_reverse.reverse()
                c_comment = c_reverse[:]
                return render(request, 'content/add_comment.html', {'cont_id':cont_id, 'c_comment':c_comment, 'user':request.user, 'messages':get_messages(request)})
            else:
                return render(request, 'content/add_comment.html', {'cont_id':cont_id, 'user':request.user, 'messages':get_messages(request)})

        else:
            return HttpResponseRedirect(reverse('site_message'))

    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))


def show_comment(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            content_id = request.POST.get('cont_id')
            if content_id:
                try:
                    c = Content.objects.get(id=int(content_id))
                except:
                    return HttpResponseRedirect(reverse('site_message'))
                else:
                    comm = c.comment_set.all()
                    c_reverse = []
                    for reverse_count in comm:
                        c_reverse.append(reverse_count)
                    c_reverse.reverse()
                    comm = c_reverse[:]
                return render(request, 'content/show_comment.html', {'comment':comm, 'user':request.user, 'messages':get_messages(request)})
            else:
                return HttpResponseRedirect(reverse('site_message'))
        else:
            return HttpResponseRedirect(reverse('site_message'))

    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def view_content_profile(request, profile_id):
    # 不考虑用post的情况下,引入权限设置
    if request.user.is_authenticated() and request.user.is_active:
        if profile_id: #and int(profile_id) == request.user.profile.id:
            try:
                p = Profile.objects.get(id=profile_id)
            except:
                messages.error(request, '请不要发出非法请求')
                return HttpResponseRedirect(reverse('site_message'))
            else:
                content = p.content_set.all().filter(circles__name='public')
                return render(request, 'content/my_mainpage.html', {'content':content, 'profile':p, 'user':request.user, 'messages':get_messages(request)})
        else:
            messages.error(request, '请查看本人的资料')
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

# def view_content_circle(request, circle_id):
#     # 不考虑用post的情况下,引入权限设置
#     if request.user.is_authenticated() and request.user.is_active:
#         if circle_id:
#             try:
#                 c = Circle.objects.get(id=circle_id)
#             except:
#                 messages.error(request, '请不要发出非法请求')
#                 return HttpResponseRedirect(reverse('site_message'))
#             else:
#                 # permission query没有存放,本来为view_vircle
#                 if request.user.has_perm('add_circle', c):
#                     content = c.content_set.all()
#                     return render(request, 'content/circle.html', {'content':content, 'circle': c, 'user':request.user, 'messages':get_messages(request)})
#                 else:
#                     messages.error(request, '您没有权限查看这个circle的资料')
#                     return HttpResponseRedirect(reverse('site_message'))
#         else:
#             return HttpResponseRedirect(reverse('site_message'))
#     else:
#         messages.error(request, '请先登录')
#         return HttpResponseRedirect(reverse('index_not_login'))

def process_thumb_up(request):
    if request.user.is_authenticated() and request.user.is_active:
        if request.method == 'POST':
            content_id = request.POST.get('thumb_up_id')
            try:
                content_id = int(content_id)
                cont = Content.objects.get(id=content_id)
                if request.user.has_perm('added_thumb_up', cont):
                    if cont.thumb_up and cont.thumb_up > 0:
                        cont.thumb_up -= 1
                    else:
                        cont.thumb_up = 0
                    remove_perm('added_thumb_up', request.user, cont)
                else:
                    assign_perm('added_thumb_up', request.user, cont)
                    if cont.thumb_up:
                        cont.thumb_up += 1
                    else:
                        cont.thumb_up = 1
                cont.save()
            except:
                messages.error(request, '请不要发出非法请求')

            return HttpResponseRedirect(reverse('site_message'))
        else:
            return HttpResponseRedirect(reverse('site_message'))
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))

def check_follower(request, user_id):
    if request.user.is_authenticated() and request.user.is_active:
        follow_lst = Follow.objects.filter(follower=int(user_id))
        user_lst = []
        for i in follow_lst:
            u = User.objects.get(id=i.followed)
            user_lst.append(u)
        return render(request, 'content/follower.html', {'follow':user_lst, 'user':request.user, 'messages':get_messages(request)})
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))
def check_followed(request, user_id):
    if request.user.is_authenticated() and request.user.is_active:
        followed_lst = Follow.objects.filter(followed=int(user_id))
        user_lst = []
        for i in followed_lst:
            u = User.objects.get(id=i.follower)
            user_lst.append(u)
        return render(request, 'content/followed.html', {'followed':user_lst, 'user':request.user, 'messages':get_messages(request)})
    else:
        messages.error(request, '请先登录')
        return HttpResponseRedirect(reverse('index_not_login'))