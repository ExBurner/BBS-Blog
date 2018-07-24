from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator, EmptyPage
import datetime
from blog.models import *

register = template.Library()


@register.inclusion_tag("get_style.html")
def get_style(username):
    """
    个人站点页面左侧区域的文章分类，
    分为:
    1.当前站点的每一个分类名称以及文章数
    2.当前站点每个标签名称以及文章数
    3.当前站点每一个年月的名称以及文章数
    :param username:
    :return:
    """
    user = User.objects.filter(username=username).first()
    if user:
        blog = user.blog

        now = datetime.datetime.now()
        both = user.create_time
        day = (now - both).days
        age = int(day / 30)  # 园龄

        #  当前站点的每一个分类名称以及文章数
        sort_list = Sort.objects.filter(blog=blog).values("sid").annotate(
            c=Count("article__aid")).values_list("title", "c")

        # 当前站点每个标签名称以及文章数
        tag_list = Tag.objects.filter(blog=blog).values("tid").annotate(
            c=Count("article__aid")).values_list("name", "c")

        # 当前站点每一个年月的名称以及文章数
        # 方式一
        # 当用到较为复杂的sql查询语句时（例如日期的阶段，大小的比较），需要用到extra(select="")方法
        # date_list = Article.objects.filter(user=user).extra(
        #     select={"Y_m_date": "date_format(create_time, '%%Y年%%c月')"}).values("Y_m_date").annotate(
        #     c=Count("aid")).values_list("Y_m_date", "c")

        # 方式二，使用django封装的TruncMonth()方法，它会将日期截断到月，抛弃后面的，接下来只需要在html中通过date标签来格式化日期格式就OK了
        """
            Article.objects.filter(user=user)
            .annotate(Y_m_date=TruncMonth("create_time"))    将日期截断至月份并加入到字段中
            .values("Y_m_date")    group by Y_m_date
            .annotate(c=Count("aid"))   select count(aid) as c
            .values_list("Y_m_date", "c")    select Y_m_date, c
        """
        date_list = Article.objects.filter(user=user) \
            .annotate(Y_m_date=TruncMonth("create_time")) \
            .values("Y_m_date") \
            .annotate(c=Count("aid")) \
            .values_list("Y_m_date", "c")

        return {"user": user, "blog": blog, "sort_list": sort_list, "tag_list": tag_list, "date_list": date_list, "age": age}


@register.inclusion_tag("back_stage/get_pages.html")
def get_pages(request, lists, style):
    """
    分类和标签的分页信息
    :param request:
    :param lists: 分类/标签 列表
    :param style: 判断 分类/标签
    :return:
    """
    paginator = Paginator(lists, 10)
    try:
        current_page = int(request.GET.get("page", 1))
        page = paginator.page(current_page)  # 获取当前页
        if paginator.num_pages > 10:
            ranges = range(current_page - 4, current_page + 5)
            if current_page - 5 < 0:
                ranges = range(1, 9)
            elif current_page + 5 > paginator.num_pages:
                ranges = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            ranges = paginator.page_range
    except EmptyPage as e:
        page = paginator.page(1)

    return {"page": page, "ranges": ranges, "current_page": current_page, "style": style}