# _*_ coding: utf-8 _*_

"""
     @author: wuxiang
     @file:adminx.py
     @time:2017/12/12 下午5:22
     这个文件是xadmin注册模型专用的
"""
import xadmin
from xadmin import views

from users.models import EmailVerifyRecord
from users.models import Banner


# 主题管理类
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "学堂在线管理系统"
    site_footer = "学堂在线"
    menu_style = "accordion"


# 注册设置类
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


class EmailVerifyRecordAdmin(object):
    # 设置列表显示的字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 设置可以检索的字段
    search_fields = ['code', 'email', 'send_type']
    # 过滤字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    # 设置列表显示的字段
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    # 设置可以检索的字段
    search_fields = ['title', 'image', 'url', 'index']
    # 过滤字段
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(Banner, BannerAdmin)
