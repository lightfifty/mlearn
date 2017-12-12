# _*_ coding: utf-8 _*_

"""
     @author: wuxiang
     @file:adminx.py
     @time:2017/12/12 下午5:22
     这个文件是xadmin注册模型专用的
"""
import xadmin

from users.models import EmailVerifyRecord


class EmailVerifyRecordAdmin(object):
    pass


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)