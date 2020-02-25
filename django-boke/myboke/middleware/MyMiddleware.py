from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


'''
中间件（类似flask 钩子函数）
    中间件应用场景
    由于中间件工作在 视图函数执行前、执行后适合所有的请求/一部分请求做批量处理。
    1、做IP限制
    放在 中间件类的列表中，阻止某些IP访问了；
    2.URL访问过滤
    如果用户访问的是login视图（放过）
    如果访问其他视图（需要检测是不是有session已经有了放行，没有返回login），这样就省得在 多个视图函数上写装饰器了！
    3、缓存(CDN)
    客户端请求来了，中间件去缓存看看有没有数据，有直接返回给用户，没有再去逻辑层 执行视图函数
'''

login_list = ['/user/center', ]

# 定义中间件类，继承MiddlewareMixin，使用需要到settings中注册
class MiddleWare1(MiddlewareMixin):
    # 重定向方法
    # 处理请求前：request对象产生之后
    def process_request(self, request):
        path = request.path
        if path in login_list:
            if not request.user.is_authenticated:
                # 如果未登陆并请求非login界面，将被重定向
                return redirect(reverse('user:login'))

    # 调用view视图函数之前
    def process_view(self, request, callback,callback_args, callback_kwargs):
        print('callback_args:',callback_args)
        print('callback_kwargs:',callback_kwargs)
        print('------------->view',callback)
        # callback(request,callback_args,callback_kwargs)

    # 调用view视图函数之后，返回response对象之前
    def process_template_response(self):
        pass

    # 处理的是响应
    def process_response(self, request, response):
        return response

    def process_exception(self,request, exception):
        pass




