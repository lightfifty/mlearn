# _*_ coding: utf-8 _*_
"""
     @author: wuxiang           
     @file:urls.py          
     @time:2017/12/13 上午11:18
"""

from django.conf.urls import url


# LoginView.as_view()，是以类的方式编写控制函数时url的写法。
from organization.views import OrgView,UserAskView

urlpatterns = [
    url(r'^$', OrgView.as_view(), name="orglist"),
    url(r'^addask/$', UserAskView.as_view(), name="addask"),
    url(r'^home/(?P<org_id>\d+)/$', UserAskView.as_view(), name="home"),
    # url(r'^login/', LoginView.as_view(), name="login"),
    # url(r'^register/', RegisterView.as_view(), name="register"),
    # url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name="active"),
    # url(r'^forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    # url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset"),
    # url(r'^modify/', ModifyPwdView.as_view(), name="modify"),

]

