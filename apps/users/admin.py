from django.contrib import admin

# Register your models here.

from .models import UserProfile


# 编写管理器

class UserProfileAdmin(admin.ModelAdmin):
    pass


# 注册数据表
admin.site.register(UserProfile, UserProfileAdmin)


