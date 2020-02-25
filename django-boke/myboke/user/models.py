from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# AbstractUser是Django自带用户认证系统，它可以处理用户账号、组、权限以及基于cookie的用户会话
class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    # icon = models.ImageField(upload_to='uploads/%Y/%m/&d')
    yunicon = models.CharField(max_length=200, default='')


    class Meta:
        db_table = 'userprofile'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name