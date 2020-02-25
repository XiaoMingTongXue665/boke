from django.forms import ModelForm
from article.models import Article


# 写文章表单
class ArticleForm(ModelForm):
    class Meta:
        # 调用models中定义的字段
        model = Article
        # 倒入全部，然后删掉不想要的
        fields = '__all__'
        exclude = ['click_num', 'love_num','user']
