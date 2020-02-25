import xadmin
from article.models import Article, Tag
from user.models import UserProfile

from xadmin import views


class BaseSettings(object):
    # 添加修改后台主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 修改logo
    site_title = '博客后台管理'
    site_footer = '浪子逐梦的博客'


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
