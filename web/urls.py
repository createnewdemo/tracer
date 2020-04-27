#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 16:03
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : urls.py
from django.conf.urls import url,include
from django.contrib import admin

from web.views import account

urlpatterns = [
    url(r'^register/$',account.register,name='register'),
]