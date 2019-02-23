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
from django.conf.urls import url
from django.views.generic import TemplateView
from users.views import *

import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    # TemplateView.asView()相当于系统会自动调用render(request,'xxx.html')进行渲染,将html文件自动转换为视图函数
    # name的作用是相当于给网址取了一个别名,主要用于反射.
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
]
