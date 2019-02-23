from datetime import datetime

from django.db import models

# 用户我要学习表单,用户咨询
from courses.models import Course
from users.models import UserProfile


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户: {0} 手机号: {1}'.format(self.name, self.mobile)


# 用户对于课程的评论
class CourseComments(models.Model):
    # 会涉及到两个外键,1.用户 2.课程 import进来
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    comments = models.CharField(max_length=250, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='评论时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户{0}对于{1}的评论: '.format(self.user, self.course)


# 用户对于课程,机构,讲师的收藏
class UserFavorite(models.Model):
    # 选择收藏的类别
    TYPE_CHOICES = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '讲师')
    )
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='数据id')
    fav_type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收藏了{1} '.format(self.user, self.fav_type)


# 用户消息表
class UserMessage(models.Model):
    # user为0的时候,发送给所有.
    user = models.IntegerField(default=0, verbose_name='接收用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})接收了{1} '.format(self.user, self.message)

# 用户课程表
class UserCourse(models.Model):
    # 会涉及两个外键: 1.用户  2.课程
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='课程')
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})学习了{1} '.format(self.user, self.course)