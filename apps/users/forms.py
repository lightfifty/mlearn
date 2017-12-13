# _*_ coding: utf-8 _*_
"""
     @author: wuxiang           
     @file:forms.py          
     @time:2017/12/13 下午7:53
      这里是是我们的表单验证类，这里面可以对表单内每个字段进行基本校验，比如长度，是否为空等。
      该类里面的每个属性名要和表单内的输入字段名称保持一致。
      基本用法如下，深入使用请查阅文档。
"""
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
