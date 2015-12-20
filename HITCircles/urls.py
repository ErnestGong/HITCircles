# -*- coding: utf-8 -*-

"""HITCircles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
import user_auth
import HITCircles
from django.contrib import admin
import content
from . import views

handler404 = 'HITCircles.views.return_404'

urlpatterns = [
    url(r'^error/$', views.return_404),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index_not_login, name='index_not_login'),
    url(r'^message/$', views.site_message, name='site_message'),
    url(r'^scrapy_show/$', views.scrapy_show, name='show_scrapy'),
    url(r'^content/', include('content.urls')),
    url(r'^',include('user_auth.urls'))
]
