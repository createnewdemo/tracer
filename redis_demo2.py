#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 23:37
# @Author  : lihanhan
# @Email   : demo1li@163.com
# @File    : redis_demo2.py
import redis
# 创建redis连接池（默认连接池最大连接数 2**31=2147483648）
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=1000)
# 去连接池中获取一个连接
conn = redis.Redis(connection_pool=pool)
# 设置键值：15131255089="9999" 且超时时间为10秒（值写入到redis时会自动转字符串）
conn.set('name', "李世林", ex=10)
# 根据键获取值：如果存在获取值（获取到的是字节类型）；不存在则返回None
value = conn.get('name')
print(value)