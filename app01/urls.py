#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 15:59
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : urls.py
from django.conf.urls import url,include
from django.contrib import admin

from app01 import views

urlpatterns = [
    url(r'^send/sms/', views.send_sms),
    url(r'^register/', views.register,name='register'),
    url(r'^index/', views.index),
]