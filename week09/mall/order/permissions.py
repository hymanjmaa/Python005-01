#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2021/1/24 16:17
"""
from rest_framework import permissions


class IsPostCreateOnly(permissions.BasePermission):
    """
    自定义权限只POST可以创建
    """
    def has_object_permission(self, request, view, obj):
        return True if request.method in ('POST') else False

