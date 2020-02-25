from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, EmailField
import re

from .models import UserProfile

# Model方法需要自己手动将表中子段导入form表单
# 生成注册表单
class UserRegisterForm(Form):
    username = forms.CharField(max_length=50, min_length=6, error_messages={'min_length': '用户名长度至少6位', }, label='用户名')
    email = forms.EmailField(required=True, error_messages={'required': '必须填写邮箱信息'}, label='邮箱')
    mobile = forms.CharField(required=True, error_messages={'required': '必须填写手机号码'}, label='手机')
    password = forms.CharField(required=True, error_messages={'required': '必须填写密码'}, label='密码',
                           widget=forms.widgets.PasswordInput)

# repassword = forms.CharField(required=True, error_messages={'required':'必须填写确认密码',}, label='确认密码', widget=forms.widgets.PasswordInput)
    #
    # BIRTH_YEAR_CHOICES = (range(1900,2020))
    # FAVORITE_COLORS_CHOICES=(
    #     ('blue','Blue'),('green','Green'),('red','Red')
    # )
    #
    # birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),label='出生日期')
    # favorite_colors = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=FAVORITE_COLORS_CHOICES,
    #     label='喜爱的颜色'
    # )

    # 验证username是否符合要求
    def clean_username(self):
        username = self.cleaned_data.get('username')
        result = re.match(r'[a-zA-Z]\w{5,}', username)
        if not result:
            raise ValidationError('用户名必须字母开头')
        return username



# ModelForm方法会自动通过model和数据表建立联系
# 验证注册表单信息
class RegisterForm(ModelForm):
    # repassword = forms.CharField(required=True, error_messages={'required':'必须填写确认密码',}, label='确认密码', widget=forms.widgets.PasswordInput)

    class Meta:
        # 方法一：直接导入想要的表字段，会直接映射到页面
        model = UserProfile
        fields = ['username', 'email', 'mobile', 'password']

        # 方法二：倒入全部，然后删掉不想要的
        # fields = '__all__'
        # exclude = ['first_name', 'date_joined', 'last_name']

    # 验证username是否符合要求
    def clean_username(self):
        username = self.cleaned_data.get('username')
        result = re.match(r'[a-zA-Z]\w{8,}', username)
        if not result:
            raise ValidationError('用户名必须字母开头')
        return username

# Model方法需要自己手动将表中子段导入form表单
# 验证登陆表单信息
class LoginForm(Form):
    username = forms.CharField(max_length=50, min_length=6, required=True, error_messages={'min_length':'用户名长度至少6位',}, label='用户名')
    password = forms.CharField(required=True, error_messages={'required':'必须填写密码',}, label='密码', widget=forms.widgets.PasswordInput)

    # class Meta:
    #     model = UserProfile
    #     fields = ['username', 'password']
    #

    # 验证登陆的用户名是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not UserProfile.objects.filter(username=username).exists():
            raise ValidationError('用户名不存在')
        return username


# 邮箱图形验证码captcha的表单
class CaptchaTestForm(forms.Form):
    email = EmailField(required=True, error_messages={'required': '必须填写邮箱'},label='邮箱')
    captcha = CaptchaField()