# _*_ coding: utf-8 _*_
"""
     @author: wuxiang           
     @file:urls.py          
     @time:2017/12/13 上午11:18
"""

from django.conf.urls import url


# LoginView.as_view()，是以类的方式编写控制函数时url的写法。
from .views import CourseListView,CourseDetailView

urlpatterns = [
    # 课程机构列表页
    url(r'^list$', CourseListView.as_view(), name="course_list"),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),




]

