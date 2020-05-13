#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 16:03
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : urls.py
from django.conf.urls import url,include
from django.contrib import admin
from web.views import home
from web.views import account

urlpatterns = [
    url(r'^register/$',account.register,name='register'),
    url(r'^login/sms/$',account.login_sms,name='login_sms'),
    url(r'^login/$',account.login,name='login'),
    url(r'^image/code$',account.image_code,name='image_code'),
    url(r'^send/sms/$',account.send_sms,name='send_sms'),
    url(r'^logout/$',account.logout,name='logout'),
    url(r'^index/$',home.index,name='index'),
]