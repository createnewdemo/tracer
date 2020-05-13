#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/13 16:44
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : auth.py
from django.utils.deprecation import MiddlewareMixin
from web import models

class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):
        """如果用户已登录  则request中赋值"""

        user_id = request.session.get('user_id', 0)
        user_obj = models.UserInfo.objects.filter(id = user_id).first()
        request.tracer = user_obj