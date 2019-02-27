from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator

from courses.models import Course
from operation.models import UserFavorite


class CourseListView(View):
    '''课程首页'''

    def get(self, request):
        # 获取所有的课程,默认按照最新的进行排序
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-students')[:3]

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作.i代表不区分大小写
            # or操作使用Q
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        # 排序功能
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 分页
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)  # 这个courses对象在前端可以通过object_list获取它里面的对象,而不能直接使用

        # 对课程进行分页,使用pure_pagination 中的Paginator模块
        context = {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
            'search_keywords': search_keywords,
        }
        return render(request, 'course-list.html', context)


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 是否有收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
                has_fav_org = True

        # 当点击课程详情页的时候,点击数需要加1
        course.click_nums += 1
        course.save()

        # 通过tag进行相关课程推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            # 因为前端是一个for循环,所以这里必须传个列表
            relate_courses = []

        context = {
            'course': course,
            'relate_courses': relate_courses,
        }
        return render(request, 'course-detail.html', context)


# 课程信息页面
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, )
