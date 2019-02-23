from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    # 自定义性别选择规则
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )

    # 昵称
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    # 生日可以为空,null=True是针对数据库的,而blank=True是针对表单的.
    # 表示该字段在数据库中可以为空,同时提交表单的时候可以,该字段可以不填.
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    # 性别,只能是男或者女.默认是女
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female', verbose_name='性别')
    # 地址
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    # 电话
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='电话')

    # 头像 默认使用default.png
    image = models.ImageField(upload_to='image%Y%m',
                              default='image/default.png',
                              max_length=100,
                              verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<UserProfile: >{}".format(self.username)


# 邮箱验证码
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱'),

    )
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    # 验证码的用途,注册和找回密码的时候都可以使用,所以要分类
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20, verbose_name='验证码类型')
    # 这里的now得去掉(),不去掉会根据编译时间。而不是根据实例化时间。
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<EmailVerifyRecord: >{}".format(self.code)


# 轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    # 保存到数据库的时候存储的是url地址
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%m', verbose_name='轮播图')
    url = models.URLField(max_length=200, verbose_name='访问地址')
    # 控制轮播图的顺序
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}(位于第{1}位)".format(self.title, self.index)
