from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from user.models import UserProfile




# 标签模块
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name

# title desc  content    date   click_num    image  love_num    author  tags


# 文章模块
class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    desc = models.CharField(max_length=256, verbose_name='简介')
    content = RichTextUploadingField(verbose_name='内容')
    date = models.DateField(auto_now=True, verbose_name='发表日期')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    love_num = models.IntegerField(default=0, verbose_name='点赞量')
    image = models.ImageField(upload_to='uploads/article/%Y/%m/%d', verbose_name='文章图片')

    tags = models.ManyToManyField(to=Tag, verbose_name='标签')
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name


# 评论模块
class Comment(models.Model):
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    content = models.TextField(verbose_name='内容')
    date = models.DateTimeField(auto_now=True, verbose_name='评论时间')

    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name='文章')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name


# 留言模块
class Message(models.Model):
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    content = models.TextField(verbose_name='内容')
    icon =models.CharField(max_length=150,verbose_name='头像',default='images/tx1.jpg')
    date = models.DateTimeField(auto_now=True, verbose_name='留言时间')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'message'
        verbose_name = '留言表'
        verbose_name_plural = verbose_name
