from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher


# 课程信息表
class Course(models.Model):
    DegreeChoices = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级')
    )
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    # 后期会替换为富文本的模式
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=DegreeChoices, max_length=2, verbose_name='课程难度')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    course_org = models.ForeignKey(CourseOrg, verbose_name='所属机构', null=True, blank=True)
    learn_time = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    category = models.CharField(max_length=20, default='', verbose_name='课程类别')
    image = models.ImageField(upload_to='courses/%Y/%m', max_length=100, verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    tag = models.CharField(max_length=15, verbose_name='课程标签', default='')
    you_need_know = models.CharField(max_length=300, default='一颗勤学的心是本课程必要前提', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, default='按时交作业,不然叫家长', verbose_name='老师告诉你')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加事件')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 章节表   课程和章节的对应关系 (一对多)->(课程对章节)
class Lesson(models.Model):
    # 外键关联
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<<{0}>>课程的章节{1}'.format(self.course, self.name)


# 视频表
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<<{0}>>章节的视频{1}".format(self.lesson, self.name)


# 课程资源表
class ResourceCourse(models.Model):
    # course相关
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name='资源名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<<{0}>> 课程的资源: {1}".format(self.course, self.name)
