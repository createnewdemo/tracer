#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 20:50
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : account.py
import random

from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection
from utils import encrypt
from web.forms.bootstrap import BootStrapForm


class RegisterModelForm(BootStrapForm,forms.ModelForm):
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length':"密码不能小于8个字符",
            'max_length':"密码不能大于64个字符",
        },
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码不能小于8个字符",
            'max_length': "重复密码不能大于64个字符",
        },
        widget=forms.PasswordInput
    )
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^^1(3|4|5|6|7|8|9)\d{9}$','手机号格式错误'),])
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

    def clean_username(self):#钩子函数
        username =self.cleaned_data['username']# 拿到数据
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已经注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data['mobile_phone']
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')  #字节转换为str

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新填写')

        return code


class SendSmsForm(forms.Form):
    """注意不是ModelForm  和数据库没关系"""
    mobile_phone = forms.CharField(label='手机号',validators=[RegexValidator(r'^^1(3|4|5|6|7|8|9)\d{9}$','手机号格式错误'),])

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_mobile_phone(self):
        """手机号校验的钩子"""
        mobile_phone = self.cleaned_data['mobile_phone']
        #判读短信模板是否有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError('短信模板错误')
        # 校验数据库中是否已有手机号
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号不存在,请注册')
        else:
            if exists:
                raise ValidationError('手机号已存在')
        #发短信  &
        code = random.randrange(1000,9999)
        sms = send_sms_single(mobile_phone,template_id,[code,])

        if sms['result'] != 0:
            raise ValidationError("短信发送失败，{}".format(sms['errmsg']))

        #写入redis  (django-redis)
        conn = get_redis_connection()
        conn.set(mobile_phone,code,ex=60)


        return mobile_phone
        #


class LoginSMSForm(BootStrapForm,forms.Form):
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^^1(3|4|5|6|7|8|9)\d{9}$', '手机号格式错误'), ])
    # ModelForm 如果发现自己类中有的字段和models.py中的字段一样 则会选择覆盖重写这个字段
    # 如果发现自己类中的存在的字段 然而models.py中没有 则会自行增加这个字段  数据库中是没有的
    code = forms.CharField(label='验证码')

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        user_obj = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not user_obj:
            raise ValidationError('手机号不存在')
        return user_obj
    def clean_code(self):
        code = self.cleaned_data['code']
        user_obj = self.cleaned_data.get('mobile_phone')
        #手机号不存在 则验证码不需要验证
        if not user_obj:
            return code
        conn = get_redis_connection()
        redis_code = conn.get(user_obj.mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')
        redis_str_code = redis_code.decode('utf-8')  # 字节转换为str
        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新填写')
        return code

class LoginForm(BootStrapForm,forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    code = forms.CharField(label='图片验证码')
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request
    def clean_password(self):

        pwd = self.cleaned_data['password']
        return encrypt.md5(pwd)
    def clean_code(self):
        """钩子 图片验证码是否正确"""
        #读取用户输入的验证吗

        code = self.cleaned_data['code']
        #去session中获取自己的验证码
        session_code = self.request.session.get('image_code')#用get 防止不存在获取不到 过期
        if not session_code:
            raise ValidationError('验证码过期，请重新获取')

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码错误')
        return code










