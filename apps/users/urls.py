# _*_ coding: utf-8 _*_
"""
     @author: wuxiang           
     @file:urls.py          
     @time:2017/12/13 上午11:18      
"""

from django.conf.urls import url, include
from users.views import LoginView, RegisterView, ActiveView,ForgetPwdView,ResetView,ModifyPwdView

# LoginView.as_view()，是以类的方式编写控制函数时url的写法。

urlpatterns = [
    url(r'^$', LoginView.as_view(), name="user_login"),
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^register/', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name="active"),
    url(r'^forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset"),
    url(r'^modify/',ModifyPwdView.as_view(),name="modify"),







]


