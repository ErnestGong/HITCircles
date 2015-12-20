# -*- coding: utf-8 -*-
from django.db import models

class Web(models.Model):
    title = models.TextField(max_length = 1000)
    link = models.TextField(max_length = 1000)
    content = models.TextField(max_length = 18000)