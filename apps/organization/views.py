# _*_ coding:utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from organization.forms import AskForm
from .models import CourseOrg, CityDict
from operaction.models import UserFavorite


# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 热门课程统计
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 城市
        all_citys = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构类别
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 筛选完后统计数量
        org_nums = all_orgs.count()

        # 对列表进行排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'course_nums':
                all_orgs = all_orgs.order_by('-courses')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        '''分页后显示的时候，在template中使用时 要用到object_list取到实际的对象。'''
        orgs = p.page(page)
        # print(orgs)
        return render(request, "org-list.html",
                      {"all_orgs": orgs, "all_citys": all_citys, "org_nums": org_nums, "city_id": city_id,
                       "category": category, "hot_orgs": hot_orgs, "sort": sort})


class UserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        askform = AskForm(request.POST)
        if askform.is_valid():
            user_ask = askform.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"填写错误！"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    get中下面几行是关于外键的操作，
    课程机构是老师表和课程表的外键，当我们想知道一个课程机构下面所有的课程和老师时，通常是拿课程机构为条件在课程表和教师表里面检索，
    但Django可以直接得到，引用该课程机构的课程列表和教师列表。
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav=True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html',
                      {'all_courses': all_courses,
                       'all_teachers': all_teachers,
                       'course_org': course_org,
                       'current_page': current_page,
                       'has_fav':has_fav
                       })


class OrgCourseView(View):
    '''机构课程页'''

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html',
                      {'all_courses': all_courses,
                       'course_org': course_org,
                       'current_page': current_page,
                       'has_fav': has_fav
                       })


class OrgDescView(View):
    '''机构介绍页'''

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',
                      {
                          'course_org': course_org,
                          'current_page': current_page,
                          'has_fav': has_fav
                      })


class OrgTeacherView(View):
    '''机构教师'''

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html',
                      {
                          'all_teachers': all_teachers,
                          'course_org': course_org,
                          'current_page': current_page,
                          'has_fav': has_fav
                      })


class AddFavView(View):
    """
    用户收藏及取消
    """

    def post(self, request):
        fav_id = int(request.POST.get('fav_id', ''))
        fav_type = int(request.POST.get('fav_type', ''))
        # 首先判断用户是否登陆了
        if not request.user.is_authenticated():
            # 如果未登陆则返回fail
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        else:
            # 如果用户已经登陆了,则查询该用户是否已经点击过收藏。
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if exist_records:
                # 如果收藏记录已经存在，则表示用户这次点击是取消收藏
                exist_records.delete()
                return HttpResponse('{"status":"success","msg":"已取消收藏"}', content_type='application/json')
            else:
                # 如果收藏记录不存在，则添加该条记录
                user_fav = UserFavorite()
                if fav_id > 0 and fav_type > 0:
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.user = request.user
                    user_fav.save()
                    return HttpResponse('{"status":"success","msg":"用户已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')
