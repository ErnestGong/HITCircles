# -*- coding: utf-8 -*-
from django.db import models

class Web(models.Model):
    title = models.TextField(max_length = 1000)
    link = models.TextField(max_length = 1000)
    content = models.TextField(max_length = 18000)

class Web1(models.Model):
    title1 = models.TextField(max_length = 1000)
    link1 = models.TextField(max_length = 1000)
    content1 = models.TextField(max_length = 18000)