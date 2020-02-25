from django.urls import path
from .views import *

app_name = 'user'

urlpatterns=[
    path('register', user_register, name='register'),  # 注册界面
    path('login', user_login, name='login'),  # 登陆界面
    path('logout', user_logout, name='logout'),  # 注销
    path('codelogin', code_login, name='codelogin'),  # 手机验证码登陆节目
    path('send_code', send_code, name='send_code'),  # 调用第三方接口，发送手机验证码
    path('forget_pwd', forget_password, name='forget_pwd'),  # 忘记密码界面
    path('valide_code', valide_code, name='valide_code'),  # 验证邮箱验证码界面
    path('update_pwd', update_pwd, name='update_pwd'),  # 更新密码界面
    path('center', user_center, name='center'),   # 本地存储
    path('center1', user_center1, name='center1'),  # 云存储
    path('zhuce', user_zhuce, name='zhuce'),
]