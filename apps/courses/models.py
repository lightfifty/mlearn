# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import models

# Create your models here.
from organization.models import CourseOrg


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="coureses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    category = models.CharField(max_length=30, verbose_name=u'课程类别', default=u'后端开发')
    tag=models.CharField(default="",verbose_name=u'课程标签',max_length=10)

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    # 该方法是定义的获取章节数目的函数，就是引用该课程的所有章节的汇总。
    def getLessonCount(self):
        count = self.lesson_set.all().count()
        return count
    # 返回学习该课程的学生,UserCourse的一个外键是course类型的。
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]



    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节名")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    name = models.CharField(max_length=100, verbose_name=u"文件名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    download = models.FileField(upload_to="courses/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
