# _*_ coding:utf-8 _*_
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email

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
            # 判断用户是否存在
            if user is not None:
                # 判断用户是否激活
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "账户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"loginform": loginform})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            # 这里其实一个先对数据中是否注册过来判断一下。

            if not UserProfile.objects.filter(email=user_name):
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()
                # 发送邮件
                send_register_email(user_name, "register")
                return render(request, "login.html", {})
            else:
                return render(request, "register.html", {"register_form": register_form, "msg": "该账户已经被注册了！"})
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "index.html")
        else:
            return render(request, "active_fail.html")


# 邮箱已经做过处理了，需要修改设置后才能使用
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email=email, send_type="forget")
            return render(request, "send_success.html", {})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
            return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 这里因为密码填错或者输入有误的时候回重复刷新页面，所以把修改的单独出来，需要对get请求和伪造的post请求进行处理，返回激活码过期。
class ModifyPwdView(View):
    def get(self, request):
        return render(request, "active_fail.html")

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get("email", "")
        if modify_form.is_valid():
            password = request.POST.get("password", "")
            password2 = request.POST.get("password2", "")
            if password != password2:
                return render(request, "password_reset.html", {"email": email, "msg": "请输入相同的密码！"})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password)
                # 这里密码修改完应该让code失效才对
                user.code = "createnull"
                user.save()
                return render(request, "login.html", {})
        else:
            if email == "":
                return render(request, "active_fail.html")
            else:
                return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})
