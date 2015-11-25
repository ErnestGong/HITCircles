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
    thumb_up = models.BigIntegerField(null=True)

class Comment(models.Model):
    profile = models.ForeignKey(Profile, null=True)
    text = models.CharField(max_length=1000)
    thumb_up = models.BigIntegerField(null=True)
    content = models.ForeignKey(Content, null=True)

class Follow(models.Model):
    follower = models.BigIntegerField(null=True)
    followed = models.BigIntegerField(null=True)
    direction = models.IntegerField(null=True)

class FollowSensor(models.Model):
    # whoto 发起人
    # censor 审核人
    whoto = models.BigIntegerField(null=True)
    censor = models.BigIntegerField(null=True)