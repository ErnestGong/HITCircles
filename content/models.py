# -*- coding: utf-8 -*-
from django.db import models
from user_auth.models import Profile, Circle
from django.contrib.auth.models import Group
# Create your models here.
# class my_Content(models.Model):
#     author = models.ForeignKey(Profile)
#     group = models.ForeignKey(Group)
#     title = models.CharField(max_length=100)
#     text = models.CharField(max_length=10000)

class Content(models.Model):
    profile = models.ForeignKey(Profile)
    circles = models.ManyToManyField(Circle)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)