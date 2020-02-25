from django.urls import path

from article.views import *

app_name = 'article'

urlpatterns = [
    path('detail', article_detail, name='detail'),  # 文章详情界面
    path('show', article_show, name='show'),
    path('write', write_article, name='write'),  # 写博客界面
    path('comment', article_comment, name='comment'),
    path('message', blog_message, name='message')
]
