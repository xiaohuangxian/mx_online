"""mx_onlie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import *
from mx_onlie.settings import MEDIA_ROOT

import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    # TemplateView.asView()相当于系统会自动调用render(request,'xxx.html')进行渲染,将html文件自动转换为视图函数
    # name的作用是相当于给网址取了一个别名,主要用于反射.
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 忘记密码的路由视图对应关系
    url(r'forget/$', ForgetView.as_view(), name='forget_pwd'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^org/', include('organization.urls', namespace='org')),
    # 激活用户url
    url(r'^active/(?P<token>.*)/$', UserActiveView.as_view(), name='user_active'),
    # 重置密码的路由视图对象关系
    url(r'^reset/(?P<token>.*)/$', ResetView.as_view(), name='reset_pwd'),
    # 修改密码提交的路由视图对象关系
    url(r'modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    url(r'^captcha/', include('captcha.urls')),  # 验证码的路由入口
    # 处理图片显示的url,使用Django自带的serve,传入参数告诉它去哪个路径找.我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
]
