from captcha.models import CaptchaStore
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.urls import reverse

from .forms import UserRegisterForm, RegisterForm, LoginForm, CaptchaTestForm
from .models import UserProfile
from .utils import util_sendmsg, send_email, upload_image
from article.models import Article

# /
# 主页视图
def index(request):
    # 按点击量到序排列
    farticles = Article.objects.all().order_by('-click_num')
    # 按时间到序排列，取前8个
    darticles = Article.objects.all().order_by('-date')[:8]
    paginator = Paginator(darticles, 3)

    return render(request, 'index.html', context={'figure_articles': farticles[:3], 'darticles': darticles})


# /user/register
# 用户注册视图
def user_register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    else:
        # 调用form表单去接受数据
        rform = RegisterForm(request.POST)
        # 判断用户是否提交了正确的数据，返回值为True
        if rform.is_valid():
            # cleaned_data以字典保存了用户输入的信息
            username = rform.cleaned_data.get('username')
            email = rform.cleaned_data.get('email')
            mobile = rform.cleaned_data.get('mobile')
            password = rform.cleaned_data.get('password')

            # 判断用户名和手机号是否已经存在
            # 不存在
            if not UserProfile.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
                # 密码加密
                password = make_password(password)
                # 注册到数据库
                user = UserProfile.objects.create(username=username, password=password, email=email, mobile=mobile)
                if user:
                    return HttpResponse('注册成功')
            # 存在
            else:
                return render(request, 'user/register.html', context={'msg': '用户名或者手机号码已经存在！'})
        print(rform.is_valid())
        return render(request, 'user/register.html', context={'msg': '注册失败，重新填写！'})



# /user/login
# 用户登陆视图
def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')
            # # 方式一：通过查询数据库验证
            # user = UserProfile.objects.filter(username=username).first()
            # # 判断登陆密码和数据库中加密的密码是否相同
            # flag = check_password(password, user.password)
            # if flag:
            #     # 保存session信息
            #     request.session['username'] = username

            # 方式二：继承了AbstractUser函数的时候可用
            # 先使用authenticate进行用户的数据库查询判断，如果有则返回用户对象
            user = authenticate(username=username,password=password)
            if user:
                # 类似session  只不过将request.user=user
                login(request, user)
                return redirect(reverse('index'))
        return render(request, 'user/login.html', context={'errors': lform.errors})

# 用户注销视图
def user_logout(request):
    # # 方式一：删除所有session信息(django session + cookie + 字典)
    # request.session.flush()

    # 方式二
    logout(request)
    return redirect(reverse('index'))

# 手机
# /user/codelogin
# 手机验证码登录视图
def code_login(request):
    if request.method == 'GET':
        return render(request, 'user/codelogin.html')
    # 获取用户提交的数据
    else:
        # 获取用户提交的手机和验证码
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')

        # 根据mobile取session值
        check_code = request.session.get(mobile)
        # 判断用户提交的验证码是否正确
        if code == check_code:
            # 从库中取出账户信息，准备登陆
            user = UserProfile.objects.filter(mobile=mobile).first()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse('验证失败!')
        else:
            return render(request, 'user/codelogin.html', context={'msg':'验证码有误!'})

# 手机
# 发送手机验证码模块  接受ajax发过来的请求，调用第三方模块给传过来的手机号码发短信
def send_code(request):
    mobile = request.GET.get('mobile')
    data = {}

    # 取出mobile所对应的所有账户信息
    if UserProfile.objects.filter(mobile=mobile).exists():
        # 调用utils中的发送手机验证码模块
        json_result = util_sendmsg(mobile)
        # 从返回的json数据中取值,状态码
        status = json_result.get('code')

        # 发送成功
        if status == 200:
            # obj字段表示此次发送的验证码
            check_code = json_result.get('obj')

            # 将验证码保存到session
            request.session[mobile]= check_code

            data['status'] = 200
            data['msg'] = '验证码发送成功'

        # 发送失败
        else:
            data['status'] = 500
            data['msg'] = '验证码发送失败'
    # 手机号不存在
    else:
        data['status'] = 501
        data['msg'] = '手机号码不存在'

    # 将成功或失败的结果的字典返回
    return JsonResponse(data)

# 邮箱
# /user/forget_pwd
# 忘记密码界面视图
def forget_password(request):
    if request.method == 'GET':
        # 使用CaptchaTestForm渲染页面
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})

    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        # 给此邮箱地址发送邮件
        result = send_email(email, request)
        return HttpResponse(result)

# 邮箱
# /user/update_pwd
# 更新修改密码视图
def update_pwd(request):
    if request.method == 'GET':
        # 获取用户的uuid，就是url后的字符串
        c = request.GET.get('c')
        # 跳转到主页面
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        # 获取用户提交的uuid
        code = request.POST.get('code')
        # 从session取出对应的用户uid
        uid = request.session.get(code)
        # 在数据库中取出uid对应的用户
        user = UserProfile.objects.get(pk=uid)

        # 获取用户提交的密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd ==repwd:
            # 将密码加密
            pwd = make_password(pwd)
            # 修改并保存密码
            user.password = pwd
            user.save()
            return render(request, 'user/update_pwd.html', context={'msg':'用户密码更新成功'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg':'更新失败'})

# 邮箱
# 定义判断验证码是否正确的路由
def valide_code(request):
    # 判断请求是否来自前端ajax
    if request.is_ajax():
        # 获取用户提交的hashkey
        key = request.GET.get('key')
        # 获取用户提交的验证码
        code = request.GET.get('code')

        # 取出数据表captcha_captchastore中hashkey值对应的验证码
        captche = CaptchaStore.objects.filter(hashkey=key).first()

        # 比较两个值是否相同
        if captche.response==code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误
            data = {'status': 0}
        return JsonResponse(data)


# 用户个人中心视图，图片保存到本地
@login_required
def user_center(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'user/center.html', context={'user': user})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        # 从表单获得图片信息，暂时保存到内存
        icon = request.FILES.get('icon')

        # 保存用户更新的信息，图片保存到本地
        user.username = username
        user.email = email
        user.mobile = mobile
        # 使用此方法更新图片需要在models中定义icon = models.ImageField(upload_to='')的方法
        user.icon = icon
        user.save()

        return render(request, 'user/center.html', context={'user': user})


# 用户个人中心视图，图片保存到云存储
# 自动验证用户是否登陆，前提必须继承AbstractUser
@login_required
def user_center1(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'user/center.html', context={'user': user})
    # 如果用户要更新数据
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        # 内存存储对象，此处表现为图片名
        icon = request.FILES.get('icon')

        # 将基本信息保存到本地数据库
        user.username = username
        user.email = email
        user.mobile = mobile

        # 将图片上传到云存储
        save_path = upload_image(icon)
        user.yunicon = save_path
        user.save()

        # 重新加载页面
        return render(request, 'user/center.html', context={'user': user})









def user_zhuce(request):
    if request.method == 'GET':
        rform = RegisterForm()
        return render(request, 'user/zhuce.html', context={'rform':rform})
    else:
        rform = UserRegisterForm(request.POST)
        rform.is_valid()
        return HttpResponse('录入成功')
