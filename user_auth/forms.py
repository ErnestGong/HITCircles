# -*- coding: utf-8 -*-

from django import forms
from .models import Circle, Profile
from django.forms.extras.widgets import SelectDateWidget

import datetime
SEX_CHOICES=(('男性', '男性'), ('女性', '女性'))
SCHOOL_CHOICES=(('计算机科学与技术','计算机科学与技术'), ('电信学院','电信学院'), ('理学院','理学院'))
GRADE_CHOICES=(('大一','大一'), ('大二','大二'), ('大三','大三'), ('大四', '大四'), ('大五', '大五'), ('研一','研一') , ('研二','研二'), ('研三', '研三'),('博一', '博一'), ('博二', '博二'), ('博三','博三'))
this_year = datetime.date.today().year
years = range(this_year - 30, this_year - 5)

circle_user_choice=[]
circle_select_choice=[]


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名:', max_length = 16, widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':'请输入姓名,不超过16个字符'}))
    password = forms.CharField(label='密码:', max_length = 16, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder':'请输入密码,不超过16个字符'}))


class PersonalInfomations(forms.Form):
    email = forms.EmailField(label='邮箱:',widget=forms.EmailInput(attrs={'placeholder':'example@example.com'}))
    sex = forms.ChoiceField(label='性别:', choices=SEX_CHOICES)
    birthday = forms.DateField(label='生日:', required=False, widget=SelectDateWidget(years=years))
    name = forms.CharField(label='真实姓名:', max_length=6, widget=forms.TextInput(attrs={'placeholder':'长度不超过6'}))
    phone_number = forms.IntegerField(label='手机号:',required=False, max_value=20000000000, widget=forms.TextInput(attrs={'placeholder':'138xxxxxxxx'}))
    nickname = forms.CharField(label='昵称:', max_length=16, widget=forms.TextInput(attrs={'placeholder':'昵称'}))
    school = forms.ChoiceField(label='学院:', choices=SCHOOL_CHOICES)
    grade = forms.ChoiceField(label='年级:', choices=GRADE_CHOICES)
    school_id = forms.IntegerField(label='学号:', max_value=9999999999, widget=forms.TextInput(attrs={'placeholder':'输入10位学号'}))
    circles = forms.MultipleChoiceField(label='Circle:', widget=forms.CheckboxSelectMultiple, choices=circle_select_choice)


class AddContent(forms.Form):
    circle_user_choice=[]
    title = forms.CharField(label='标题:', max_length=30, widget=forms.TextInput(attrs={'placeholder':'请输入标题,仅限30字'}))
    content = forms.CharField(label='内容:', max_length=1000, widget=forms.Textarea(attrs={'placeholder':'请输入文章内容,仅限1000字'}))
    circle = forms.MultipleChoiceField(label='Circle:', widget=forms.CheckboxSelectMultiple, choices=circle_user_choice)