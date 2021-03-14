#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('logout', views.logout_v),
    path('publish', views.publish),
    re_path(r'^article/(?P<aid>\d+)/', views.article),
    re_path(r'^article_del/(?P<aid>\d+)/', views.article_del),
    re_path(r'^edit/(?P<aid>\d+)/', views.article_edit),
    re_path(r'^reply/(?P<rtype>\d+)/(?P<aid>\d+)/', views.reply),
    path('edit_info/', views.edit_info),
]
