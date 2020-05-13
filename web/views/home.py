#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 16:15
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : home.py
from django.shortcuts import redirect,render,HttpResponse

def index(request):
    return render(request,'index.html')