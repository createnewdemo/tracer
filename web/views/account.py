#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 12:08
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : account.py
from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from web.forms.account import RegisterModelForm
"""
用户账户相关功能：注册 登录 短信 注销
"""



def register(request):
    form = RegisterModelForm()
    return render(request,'register.html',{'form':form})