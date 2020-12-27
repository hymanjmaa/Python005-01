#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2020/12/27 12:32
"""
import redis
from datetime import datetime
import time


redis_conn = redis.Redis(host='127.0.0.1', port=6379, password='root')
PHONE_LIMIT_CONFIG = {132110119120111: 3}


def send_times(func):
    def inner_todo(*args, **kwargs):
        telephone_number = args[0]
        phone_ct = redis_conn.get(telephone_number)
        if phone_ct is None or int(phone_ct) < PHONE_LIMIT_CONFIG[telephone_number]:
            func(*args, **kwargs)
            counter(str(telephone_number))
        else:
            print('此手机号已达最大限制')

    return inner_todo


@send_times
def sendsms(telephone_number: int, content: str, key=None):
    ct = redis_conn.get(key)
    if ct is None or int(ct.decode()) < 5:
        sms_content_check(telephone_number, content)
        counter(key)
    else:
        print('请勿频繁发送，请1分钟后重试')


def gen_counter_key(telephone_number):
    return '{}_{}'.format(telephone_number, datetime.utcnow().strftime('%Y%m%d%H%M'))


def counter(key):
    redis_conn.incr(key)
    redis_conn.expire(key, 90)
    return redis_conn.get(key).decode()


def send_msg(telephone_number, content):
    print(f'send sms msg: {telephone_number}, {content}')


def sms_content_check(telephone_number, content):
    if len(content) > 70:
        while len(content) > 0:
            sub_content = content[:70]
            content = content[70:]
            send_msg(telephone_number, sub_content)
    else:
        send_msg(telephone_number, content)


if __name__ == '__main__':
    for x in range(20):
        tn = 132110119120111
        sendsms(tn, 'Tip Tip Pretty Girl Coming...'*10, gen_counter_key(tn))
        time.sleep(5)

