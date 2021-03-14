from django.db import models

# Create your models here.


class User(models.Model):

    user_name = models.CharField(verbose_name='用户名', max_length=64, unique=True)
    nick_name = models.CharField(verbose_name='昵称', max_length=64)
    mail = models.CharField(verbose_name='邮箱', max_length=64)
    desc = models.CharField(verbose_name='简介', max_length=256)
    password = models.CharField(verbose_name='密码', max_length=16)
    score = models.IntegerField(verbose_name='积分')
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)


class Article(models.Model):

    user_id = models.IntegerField(verbose_name='用户id')
    mark = models.CharField(verbose_name='标签', max_length=256)
    title = models.CharField(verbose_name='帖子标题', max_length=64)
    content = models.CharField(verbose_name='帖子正文', max_length=1024)
    img = models.CharField(verbose_name='帖子图片', max_length=128, null=True)
    intro = models.CharField(verbose_name='帖子简介', max_length=256)
    view_n = models.IntegerField(verbose_name='阅读数')
    is_delete = models.BooleanField(verbose_name='是否删除')
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateField(verbose_name='更新时间', auto_now_add=True)


class Reply(models.Model):

    REPLY_ARTICLE = 1
    REPLY_REPLY = 2

    r_type = models.IntegerField(verbose_name='回复类型')
    user_id = models.IntegerField(verbose_name='用户id', null=True)
    pid = models.IntegerField(verbose_name='parent id')
    img = models.CharField(verbose_name='回复图片', max_length=128, null=True)
    content = models.CharField(verbose_name='回复内容', max_length=256)
    create_time = models.DateField(verbose_name='留言时间', auto_now_add=True)
    update_time = models.DateField(verbose_name='更新时间', auto_now_add=True)


class Notice(models.Model):

    a_title = models.CharField(verbose_name='公告标题', max_length=64)
    a_content = models.CharField(verbose_name='公告内容', max_length=3000, null=True)
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
