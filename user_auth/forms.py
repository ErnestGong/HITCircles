# -*- coding: utf-8 -*-

from django import forms
from .models import Circle, Profile
from django.forms.extras.widgets import SelectDateWidget

import datetime
SEX_CHOICES=(('男性', '男性'), ('女性', '女性'))
SCHOOL_CHOICES=(('计算机科学与技术','计算机科学与技术'), ('电信学院','电信学院'), ('理学院','理学院'))
GRADE_CHOICES=(('大一','大一'), ('大二','大二'), ('大三','大三'), ('大四', '大四'), ('大五', '大五'), ('研一','研一') , ('研二','研二'), ('研三', '研三'),('博一', '博一'), ('博二', '博二'), ('博三','博三'))
FOLLOW_AUTH_CHOICES=(('free', '允许关注'), ('censor', '关注前需要经过审核'), ('forbidden', '拒绝关注'))
this_year = datetime.date.today().year
years = range(this_year - 30, this_year - 5)

circle_user_choice=[]
circle_select_choice=[]


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名:', max_length = 16, widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':'用户名(少于16个字符)'}))
    password = forms.CharField(label='密码:', max_length = 16, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder':'密码(少于16个字符)'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名:', max_length = 16, widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':'用户名(少于16个字符)'}))
    password = forms.CharField(label='密码:', max_length = 16, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder':'密码(少于16个字符)'}))
    password_reconfirm = forms.CharField(label='再次确认密码:', max_length = 16, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder':'请确认密码'}))


class PersonalInfomations(forms.Form):
    email = forms.EmailField(label='邮箱:',widget=forms.EmailInput(attrs={'placeholder':'example@example.com(必填)'}))
    sex = forms.ChoiceField(label='性别:', widget=forms.Select(attrs={'class':'ui fluid dropdown'}) ,choices=SEX_CHOICES)
    birthday = forms.DateField(label='生日:', required=False, widget=SelectDateWidget(years=years, attrs={'class':'field ui fluid dropdown'}))
    name = forms.CharField(label='真实姓名:', max_length=6, widget=forms.TextInput(attrs={'placeholder':'长度不超过6(必填)'}))
    phone_number = forms.IntegerField(label='手机号:',required=False, max_value=20000000000, widget=forms.TextInput(attrs={'placeholder':'138xxxxxxxx'}))
    nickname = forms.CharField(label='昵称:', max_length=16, widget=forms.TextInput(attrs={'placeholder':'昵称(必填)'}))
    school = forms.ChoiceField(label='学院:', widget=forms.Select(attrs={'class':'ui fluid dropdown'}), choices=SCHOOL_CHOICES)
    grade = forms.ChoiceField(label='年级:', widget=forms.Select(attrs={'class':'ui fluid dropdown'}), choices=GRADE_CHOICES)
    school_id = forms.IntegerField(label='学号:', max_value=9999999999, widget=forms.TextInput(attrs={'placeholder':'输入10位学号(必填)'}))
    circles = forms.MultipleChoiceField(label='Circle:', widget=forms.CheckboxSelectMultiple, choices=circle_select_choice)
    follow_auth = forms.ChoiceField(label='他人关注权限:', choices=FOLLOW_AUTH_CHOICES, widget=forms.RadioSelect)


class AddContent(forms.Form):
    circle_user_choice=[]
    title = forms.CharField(label='标题:', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'请输入标题,仅限30字(必填)','style':'width:90%;resize:none;'}))
    content = forms.CharField(label='内容:', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'请输入文章内容,仅限1000字(必填)','style':'width:90%;height:100px;resize:none;'}))
    circle = forms.ChoiceField(label='Circle:', widget=forms.RadioSelect, choices=circle_user_choice)