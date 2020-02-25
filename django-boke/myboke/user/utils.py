import hashlib
import os
import uuid
from time import time

import json
import requests


from django.core.mail import send_mail
from myboke.settings import EMAIL_HOST_USER, MEDIA_ROOT
from qiniu import Auth, put_data

from .models import UserProfile

# 作用就是向网易云信发送请求，帮助后台发送短信息给客户
def util_sendmsg(mobile):
    # 访问网易云信的url地址
    url = 'https://api.netease.im/sms/sendcode.action'
    # 传过来的的手机号码
    data = {'mobile': mobile}
    # 4部分组成 headers： AppKey  Nonce  CurTime  CheckSum
    AppKey = '4e185a4211ffb942ce1bf243ba99ae01'
    Nonce = '8wfsdg8sdg8s8dg85656ffasf'
    CurTime = str(time())

    AppSecret = '17e9dbcf5938'
    content = AppSecret + Nonce + CurTime
    CheckSum = hashlib.sha1(content.encode('utf-8')).hexdigest()

    # 打包headers中的信息
    headers = {'AppKey': AppKey, 'Nonce': Nonce, 'CurTime': CurTime, 'CheckSum':CheckSum}

    # 发送requset请求，获得响应体
    response = requests.post(url, data, headers=headers)

    print(response)

    # 获得响应体中的数据，字符串格式
    str_result = response.text

    # 转换成json格式
    json_result = json.loads(str_result)

    return json_result


# 发送邮件工具
def send_email(email, request):
    subject = '个人博客找回密码'
    user = UserProfile.objects.filter(email=email).first()
    # 使用uuid生成随机值
    ran_code = uuid.uuid4()
    ran_code = str(ran_code)
    ran_code =ran_code.replace('-','')

    # 将uuid的随机值保存到session中
    request.session[ran_code]=user.id

    # 邮件内容
    message = '''
     可爱的用户:
            您好！此链接用户找回密码，请点击链接: <a href='http://127.0.0.1:8000/user/update_pwd?c=%s'>更新密码</a>，
            如果链接不能点击，请复制：
            http://127.0.0.1:8000/user/update_pwd?c=%s

           个人博客团队
    ''' % (ran_code, ran_code)

    # 发送邮件接收返回值
    result = send_mail(subject, "", EMAIL_HOST_USER, [email, ],html_message=message)
    return result


# 上传图片到云存储
def upload_image(storeobj):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'gAfs4XKMy8-Tf3_JotL6hCqaQkKX2FVM21usVbWR'
    secret_key = 'KUhYH1TSnLQiB44tjGE1v09fzGqtdS4nS8f4Uhr7'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'zygboke'

    # 上传后保存的文件名
    key = storeobj.name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 将图片推送到云存储
    ret, info = put_data(token, key, storeobj.read())

    # 获取保存后的文件名
    filename = ret.get('key')
    # 拼接图片访问路径给前端使用
    save_path = 'http://q5p4gw7j9.bkt.clouddn.com/'+filename
    return save_path