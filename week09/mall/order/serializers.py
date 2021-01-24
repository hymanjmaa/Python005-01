#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2021/1/24 14:52
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Order
User = get_user_model()


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    buyer_id = serializers.ReadOnlyField(source='buyer_id.username')
    is_delete = serializers.ChoiceField(choices=Order.DELETE_SELECT)

    class Meta:
        model = Order
        fields = ['url', 'order_id', 'product_id', 'buyer_id', 'create_time', 'is_delete']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """用户序列"""
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'orders']