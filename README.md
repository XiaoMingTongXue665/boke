## 使用Django快速搭建博客

# 要求  
Python: 3.5+  
Django: 2.x  
Mysql  

# 功能介绍  
Django 自带的后台管理系统，方便对于文章、用户及其他动态内容的管理  
文章分类、标签、浏览量统计  
用户认证系统  
文章评论系统，炫酷的输入框特效，支持 markdown 语法，二级评论结构和回复功能  
信息提醒功能，登录和退出提醒，收到评论和回复提醒  

# 下载  
wget https://github.com/15830900798/boke.git  
or  
git clone git@github.com:15830900798/boke.git  

# 安装  
pip install -r requirements.txt  #安装所有依赖  
setting.py配置自己的数据库  
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  

# 使用  
## 初始化用户名密码  
python manage.py createsuperuser  
按照提示输入用户名、邮箱、密码即可  
## 登录后台 编辑类型、标签、发布文章等  
http://ip:port/  
