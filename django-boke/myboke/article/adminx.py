import xadmin
from article.models import Article, Tag


# 增加文章表的功能
class ArticleAdmin(object):
    # 在主页显示以下字段
    list_display = ['title', 'click_num', 'love_num', 'user']
    # 添加检索框，可以检索以下字段内容
    search_fields= ['title','id','content']
    # 在主页就可以编辑一下子段
    list_editable= ['click_num','love_num']
    # 添加过滤器，可以过滤以下字段
    list_filter=['date','user']


xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Tag)
