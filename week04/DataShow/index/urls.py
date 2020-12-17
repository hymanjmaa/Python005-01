#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2020/12/17 22:26
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index)
]
