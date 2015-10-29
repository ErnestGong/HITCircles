from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from . import models
# Create your views here.

def site_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('site_message'))
            else:
                return HttpResponseRedirect(reverse('index_not_login'))
        else:
            return HttpResponseRedirect(reverse('index_not_login'))
    else:
        return HttpResponseRedirect(reverse('index_not_login'))


def site_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            try:
                u_registered = User.objects.get(username=username)
            except:
                u = User.objects.create_user(username=username,password=password)
                u.save()
                return render(request, 'user/register.html', {'username':username, 'password':password, 'message':'Please fill in more infomations'})
            else:
                # u_registered = User.objects.get(username=username)
                try:
                    email=request.POST['email']
                    sex=request.POST['sex']
                    year=request.POST['year']
                    month=request.POST['month']
                    day=request.POST['day']
                except:
                    return render(request, 'user/register.html', {'username':username, 'password':password, 'message':'Please fill in every blank'})
                # store more details about a user's profile
                else:
                    u_registered.email=email
                    # if sex == 'True':
                    #     u_registered.profile.sex=True
                    # elif sex == 'False':
                    #     u_registered.profile.sex=False
                    # if year.isdigit() and year >= 1000 and year <= 3000:
                    #     u_registered.profile.birthday.year=year
                    # if year.isdigit() and year >= 1 and year <= 12:
                    #     u_registered.profile.birthday.month=month
                    # if year.isdigit() and year >= 1 and year <= 31:
                    #     u_registered.profile.birthday.day=day
                    u_registered.save()
                    return HttpResponseRedirect(reverse('index_not_login'))
        else:
            return render(request, 'user/register.html',{'message':'Please fill in the blanks', 'username':'', 'password':''})

    else:
        return render(request, 'user/register.html',{'message':'Please fill in the blanks', 'username':'', 'password':''})

def site_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index_not_login'))