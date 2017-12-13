# _*_ coding:utf-8 _*_
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm

# Create your views here.

"""由于这里我们的用户管理使用的是Django自带的用户管理，所以我们可以直接使用其用户登陆和验证的方法"""


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


"""
LoginView 类是处理登陆请求的处理类，内部主要封装get和post方法，具体使用示例如下：
针对以post方式提交的表单，我们先用form进行字段验证，is_valid()方法返回验证结果。
form验证通过后再进行用户登陆验证的逻。
"""


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"loginform": loginform})

# 函数式控制逻辑
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg": "用户名或密码错误"})
#     elif request.method == "GET":
#         return render(request, "login.html")
