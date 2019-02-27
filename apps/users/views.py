from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View

from users.models import UserProfile, EmailVerifyRecord
from util.send_email import send_register_email
from .forms import *


class LoginView(View):
    def post(self, request):
        # 1.先使用表单进行验证
        # POST中的username和password,会对应到form表单中
        login_form = LoginForm(request.POST)

        # 2.如果表单验证成功,获取用户名和密码
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 3.利用Django的认证模块,进行用户认证.
            user = authenticate(username=username, password=password)

            if user:
                # auth模块的login方法,两个参数request和user
                # 实际上是duirequest谢了一部分东西进去,然后再render的时候
                # request要是render回去的.这些信息也就随着返回给浏览器,完成登录
                # 4.如果认证成功,就调用Django的login方法进行登录,可以自动保存session和cookie
                login(request, user)
                return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:

            return render(request, 'login.html', {'login_form': login_form})

    def get(self, request):
        return render(request, 'login.html', {})


class RegisterView(View):
    def get(self, request):
        # 添加验证码,RegisterForm会为我们生成输入框+验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')

            # 实例化一个user_profile对象,将前台的值传入
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username

            # 加密password进行保存
            user_profile.password = make_password(password)
            user_profile.is_active = False  # 默认不是激活状态
            user_profile.save()

            # 发送激活链接
            send_register_email(username, 'register')
            # 激活成功跳转到登录界面
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'err': '用户名或密码错误'})


# 处理用户激活的类视图
class UserActiveView(View):
    def get(self, request, token):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=token)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)

        # 如果不为空就说明是合法的token
        if all_record and active_form:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return redirect(reverse('login'))
        return render(request, 'register.html', {'msg': '你的激活链接无效', 'active_form': active_form})


# 忘记密码的类视图
class ForgetView(View):
    def get(self, request):
        forgetForm = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forgetForm})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'login.html', {'msg': '重置密码邮件已经发送'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码的试图类
class ResetView(View):
    def get(self, request, token):
        # 传邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=token)
        # 进行表单验证
        active_form = ActiveForm(request.GET)

        if all_record and active_form:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'forgetpwd.html', {'msg': '你的重置密码链接无效'})


# 提交修改密码的视图类
class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html', {'msg': '密码修改成功,重新登录'})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modifypwd_form': modifypwd_form})


class UserInfoView(View):
    pass


class LogoutView(View):
    pass


class MyMessageView(View):
    pass
