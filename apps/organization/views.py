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
        orgs = p.page(page)

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
    """
    def get(self,request,org_id):
        course_org=CourseOrg.objects.get(id=int(org_id))
