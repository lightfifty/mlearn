# _*_ coding:utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from organization.forms import AskForm
from .models import CourseOrg, CityDict


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
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html',
                      {'all_courses': all_courses,
                       'all_teachers': all_teachers,
                       'course_org':course_org
                       })


