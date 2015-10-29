from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.urlresolvers import reverse
import datetime
from django.http import HttpResponseRedirect
from django.utils import timezone


def index_not_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('site_message'))
    else:
        return render(request, 'user/index_not_login.html')

def site_message(request):
    if request.user.is_authenticated():
        return render(request, 'user/message.html', {'username':request.user.username, 'status':'logged in', 'profile':request.user})
    else:
        return render(request, 'user/message.html', {'username':'Please log in', 'status':'', 'profile':''})