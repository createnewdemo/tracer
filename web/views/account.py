#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 12:08
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : account.py
from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.conf import settings
from django.http import JsonResponse
from web import models
from django.db.models import Q

"""
用户账户相关功能：注册 登录 短信 注销
"""


def register(request):
    """注册"""
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过  写入数据库（密码要是密文）
        # form.instance.password = "awdawdawd"
        form.save()  # 会自动剔除数据库中没用的字段
        # instance = models.UserInfo.objects.create(**form.cleaned_data) #和上面的是一样的但是要手动剔除字典中的数据 pop
        return JsonResponse({'status': True, 'data': '/login/sms/'})
    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号不能为空 格式是否正确
    if form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    """短信登陆"""
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入正确 登录成功
        user_obj = form.cleaned_data['mobile_phone']
        print(user_obj)
        request.session['user_id'] = user_obj.id
        request.session['user_name'] = user_obj.username
        return JsonResponse({'status': True, 'data': '/index/'})
    return JsonResponse({'status': False, 'data': form.errors})


def login(request):
    """用户名与密码登录"""
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # user_obj = models.UserInfo.objects.filter(username=username,password=password).first()
        user_obj = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
            password=password).first()
        if user_obj:
            # 用户名秘密正确
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('index')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """生成图片验证码"""
    from io import BytesIO
    from utils.image_code import check_code

    image_obj, code = check_code()

    request.session['image_code'] = code
    request.session.set_expiry(60)
    stream = BytesIO()
    image_obj.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()

    return redirect('index')