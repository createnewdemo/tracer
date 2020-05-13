#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 22:52
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : bootstrap.py
class BootStrapForm():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
