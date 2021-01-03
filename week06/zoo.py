#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2021/1/3 13:30
"""
from abc import ABCMeta


BODY_TYPE_DEFINE = {'小': 1, '中': 2, '大': 3}


class Zoo(object):

    def __init__(self, name):
        self.name = name

    def add_animal(self, animal):
        animal_cls = type(animal).__name__
        if animal_cls in self.__dict__:
            print('{}已存在'.format(animal_cls))
        else:
            self.__dict__[animal_cls] = animal_cls


class Animal(metaclass=ABCMeta):

    def __init__(self, a_type, body_type, nature):
        self.a_type = a_type
        self.body_type = body_type
        self.nature = nature

    def check_is_ferocious(self):
        return self.body_type >= BODY_TYPE_DEFINE['中'] and self.a_type == '食肉' and self.nature == '凶猛'


class Cat(Animal):
    voice = '妙妙'

    def __init__(self, name, a_type, body_type, nature):
        super().__init__(a_type, body_type, nature)
        self.name = name

    def is_pet(self):
        return not super().check_is_ferocious()


class Dog(Animal):
    voice = '旺旺'

    def __init__(self, name, a_type, body_type, nature):
        super().__init__(a_type, body_type, nature)
        self.name = name

    def is_pet(self):
        return not super().check_is_ferocious()


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    print(have_cat)
    have_dog = hasattr(z, 'Dog')
    print(have_dog)
