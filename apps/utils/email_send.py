# _*_ coding: utf-8 _*_
"""
     @author: wuxiang           
     @file:email_send.py          
     @time:2017/12/14 上午11:37      
"""
from random import Random

from django.core.mail import send_mail

from mlearn.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def random_str(randomlength=8):
    str = ''
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/users/active/{0}'.format(code)
    elif send_type == "forget":
        email_title = "慕学在线网密码找回链接"
        email_body = '请点击下面的链接找回你的账号：http://127.0.0.1:8000/users/active/{0}'.format(code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        # 发送成功
        pass
    else:
        pass
