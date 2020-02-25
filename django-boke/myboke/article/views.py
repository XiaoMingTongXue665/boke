from django.contrib.auth.decorators import login_required
from django.core.checks import Tags
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


from article.forms import ArticleForm
from article.models import Article, Tag, Comment, Message





# 文章详情视图
def article_detail(request):
    # 获取用户点击页面的id
    id = request.GET.get('id')
    print(id)
    # pk全称primary key(主键)
    article = Article.objects.get(pk=id)


    # 将点击量加1
    article.click_num += 1
    article.save()

    # 底部的相关文章模块
    # 获取当前文章所有tag
    tags_list = article.tags.all()
    # 便利相同有相同tag的文章标题显示，保留6个
    list_about = []
    for tag in tags_list:
        for article in tag.article_set.all():
            if article not in list_about and len(list_about) < 6:
                list_about.append(article)

    # 查询评论数
    comments = Comment.objects.filter(article_id=id)

    return render(request, 'article/info.html',context={'article': article, 'list_about': list_about, 'comments': comments})

# 学无止境视图
def article_show(request):
    # 显示顶部标签，保留前6个
    tags = Tag.objects.all()[:6]
    tid= request.GET.get('tid','')
    # 点击标签后，查询返回相应界面
    # 如果有标签，返回拥有此标签的所有文章
    if tid:
        tag=Tag.objects.get(pk=tid)
        # 根据标签去查文章
        articles = Article.objects.filter(tags__name=tag.name)
    # 如果没有，返回所有文章
    else:
        articles = Article.objects.all()

    # 分页器，没页显示3条数据
    paginator = Paginator(articles, 3)
    print(paginator.count)  # 总的条目数  总的记录数
    print(paginator.num_pages)  # 可以分页的数量  总的页码数
    print(paginator.page_range)  # 页面的范围



    # 分页器方法： get_page()
    # 底部页码，默认返回第一页
    page_number = request.GET.get('page', 1)
    # 传页码数
    page = paginator.get_page(page_number)  # 返回的是page对象
    # page.has_next()  # 有没有下一页
    # page.has_previous()  # 判断是否存在前一页
    # page.next_page_number() # 获取下一页的页码数
    # page.previous_page_number() # 获取前一页的页码数

    #属性：
    # object_list   当前页的所有对象
    # number       当前的页码数
    # paginator     分页器对象

    return render(request, 'article/learn.html', context={'page': page, 'tags': tags, 'tid': tid})

# 写博客视图
@login_required
def write_article(request):
    if request.method == 'GET':
        # 调用写博客表单
        aform = ArticleForm()
        return render(request, 'article/write.html', context={'form': aform})
    else:
        # 接受用户提交的数据
        aform = ArticleForm(request.POST, request.FILES)
        # 判断数据是否存在
        if aform.is_valid():
            # cleaned_data中保存了用户所有提交了的数据
            # 1对多 直接赋值
            data = aform.cleaned_data
            article = Article()
            article.title = data.get('title')
            article.desc = data.get('desc')
            article.content = data.get('content')

            article.image = data.get('image')
            article.desc = data.get('desc')
            article.user = request.user
            article.save()

            # 多对多 必须添加到文章保存的后面添加
            article.tags.set(data.get('tags'))
            # 保存成功后重定向到首页
            return redirect(reverse('index'))

        # 数据不正确重定向，继续填写
        return render(request, 'article/write.html', context={'form': aform})

# 文章评论视图
def article_comment(request):
    # 直接接受
    nickname = request.GET.get('nickname')
    content = request.GET.get('saytext')
    aid = request.GET.get('aid')

    # 保存入库
    comment = Comment.objects.create(nickname=nickname, content=content, article_id=aid)

    # 保存成功
    if comment:
        data = {'status': 1}
    else:
        data = {'status': 0}
    return JsonResponse(data)


# 留言视图
def blog_message(request):
    # 查询所有留言
    messages = Message.objects.all()
    # 调用分页器，没页显示8个
    paginator = Paginator(messages, 8)
    # 获取页码数
    page = request.GET.get('page', 1)
    print(page)
    # 得到page对象
    page = paginator.get_page(page)
    print(page)

    if request.method == 'GET':
        return render(request, 'article/lmessage.html', context={'page':page})
    else:
        # 获取用户提交的留言
        name = request.POST.get('name')
        mycall = request.POST.get('mycall')
        lytext = request.POST.get('lytext')
        if name and lytext:
            message = Message.objects.create(nickname=name, icon=mycall, content=lytext)
            if message:
                return redirect(reverse('article:message'))
        return render(request, 'article/lmessage.html', context={'page':page, 'error': '必须输入用户名和内容'})
