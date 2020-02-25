"""myboke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from user.views import index
from django.views.static import serve
from .settings import MEDIA_ROOT
import xadmin

urlpatterns = [
    path('xadmin/', xadmin.site.urls),  # xadmin后台管理界面
    path('', index, name='index'),  # 主页界面
    path('user/', include('user.urls', namespace='user')),
    path('article/', include('article.urls', namespace='article')),
    re_path(r'^captcha/', include('captcha.urls')),  # 前端文字验证码路由
    # 添加前端引用库中图片位置的路由
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 加载ckeditor的urls
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

