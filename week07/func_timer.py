#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2021/1/17 12:08
"""
from functools import wraps
from datetime import datetime
import requests


def f_timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = datetime.now()
        try:
            return func(*args, **kwargs)
        finally:
            cost = (datetime.now() - start).total_seconds()
            print(f"cost time: {cost} s")

    return inner


@f_timer
def req_url(url):
    resp = requests.get(url)
    print('req_done')


if __name__ == '__main__':
    req_url('http://www.baidu.com')
