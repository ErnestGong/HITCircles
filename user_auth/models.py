# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField(null=True)
    sex = models.CharField(max_length=10, null=True)
    phone_number = models.BigIntegerField(null=True)
    nickname = models.CharField(max_length=100, null=True)
    school = models.CharField(max_length=100, null=True)
    grade = models.CharField(max_length=10, null=True)
    school_id = models.BigIntegerField(null=True)
    follow_count = models.BigIntegerField(null=True)
    followed_count = models.BigIntegerField(null=True)
    censor_count = models.BigIntegerField(null=True)
    class Meta:
        permissions = (
            ("open_relationship", "Can follow freely"),
            ("censor_relationship", "Can follow if the user agreed"),
        )

class Circle(models.Model):
    name = models.CharField(max_length=100)
    statement = models.CharField(max_length=1000)
    profile = models.ManyToManyField(Profile)

class PendingRequest(models.Model):
    circle_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)