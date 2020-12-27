#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2020/12/27 11:19
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.video_detail),
    path('click_video', views.click_video)
]
