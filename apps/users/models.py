# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# 系统内部有一个User 我们可以使用该类作为基类，自己添加一些特殊的字段就可以，比较特殊的是imagefield 其实是一个字符类型，unicode是为了方便打印。


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='boby')
    birday = models.DateField(verbose_name=u'生日', null=True)
    gender = models.CharField(choices=(("male", u"男"), ("female", "女")), default="female", max_length=10)
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register", u"注册"), ("forget", u"找回密码")), max_length=10,
                                 verbose_name=u"验证码类型")
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}({1})".format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
