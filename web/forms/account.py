#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 20:50
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : account.py
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^^1(3|4|5|6|7|8|9)\d{9}$','手机号格式错误'),])
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput)
    # ModelForm 如果发现自己类中有的字段和models.py中的字段一样 则会选择覆盖重写这个字段
    # 如果发现自己类中的存在的字段 然而models.py中没有 则会自行增加这个字段  数据库中是没有的
    code = forms.CharField(label='验证码')
    class Meta:
        model = models.UserInfo#这里一定是model  没有s
        fields = ['username','email','password','confirm_password','mobile_phone','code']
    def __init__(self,*args,**kwargs):#每次实例化字段都会执行__init__方法的
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' %(field.label)