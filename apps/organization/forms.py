# _*_ coding: utf-8 _*_
"""
     @author: wuxiang           
     @file:forms.py          
     @time:2017/12/23 下午9:54      
"""
import re
from django import forms

from operaction.models import UserAsk

"""
传统的表单验证
"""

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, max_length=50)


"""
使用Model form
"""


class AskForm(forms.ModelForm):
    """这里可以新增表单验证的字段"""

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
