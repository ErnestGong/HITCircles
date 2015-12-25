# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.site_login, name='site_login'),
    url(r'^register/$', views.site_register, name='site_register'),
    url(r'^add_infomation', views.add_infomation, name='add_infomation'),
    url(r'^logout/$', views.site_logout, name='site_logout'),
    url(r'^auth_request/$', views.permission_request, name='permission_request'),
    url(r'^auth_reject_request/$', views.permission_reject_request, name='permission_reject_request'),
    url(r'^search/$', views.search_to_follow, name='search_to_follow'),
    url(r'^add_follow/$', views.add_follow, name='add_follow'),
    url(r'^censor_follow/$', views.censor_follow, name='censor_follow'),
    url(r'^delete_follow/$', views.delete_follow, name='delete_follow'),
    url(r'^reject_follow/$', views.reject_follow, name='reject_follow'),
    url(r'^add_circle/$', views.add_circle, name='add_circle'),
]