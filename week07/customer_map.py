#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2021/1/17 12:08
"""


def cmap(func, *iterables):
    l = [iter(i) for i in iterables]
    while True:
        try:
            yield func(*[next(i) for i in l])
        except StopIteration:
            return


if __name__ == '__main__':
    print(list(map(lambda x: x + 1, [1, 4, 9])))
    print(list(cmap(lambda x: x + 1, [1, 4, 9])))
