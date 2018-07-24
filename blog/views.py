from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.db import transaction
import json
import os
from bs4 import BeautifulSoup
from .utils.geetest import GeetestLib
from .utils.verify_code import *
from .my_forms import *
from cnblog.settings import MEDIA_ROOT
from .utils.pages import get_pages


pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


@csrf_exempt
def login(request):
    """
    用户登录
    1.获取滑动验证码
    2.获取用户名和密码并进行校对，如果错误返回错误信息，成功则返回登录界面
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == 'POST':
        # 滑动验证码，利用geetest插件
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        username = request.POST.get("username")
        password = request.POST.get("password")
        response = {"user": None, "msg": None}
        if status:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                response["user"] = user.username
            else:
                response["msg"] = "用户名或者密码错误！"
        return JsonResponse(response)

        # 图片验证码
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # verify_codes = request.POST.get("verify_code")
        # verify_code_str = request.session.get("verify_code_str")
        # response = {"user": None, "msg": None}
        # if verify_codes.upper() == verify_code_str.upper():
        #     user = auth.authenticate(username=username, password=password)
        #     if user:
        #         auth.login(request, user)
        #         response["user"] = user.username
        #     else:
        #         response["msg"] = "用户名或者密码错误！"
        # else:
        #     response["msg"] = "验证码错误！"
        # return JsonResponse(response)


def verify_code(request):
    """
    获取图片验证码
    :param request:
    :return:
    """
    data = get_verify_code(request)
    return HttpResponse(data)


def index(request):
    """
    博客主界面，主要传入分页之后的文章列表
    :param request:
    :return:
    """
    article_list = Article.objects.all().order_by("-create_time")
    ret = get_pages(request, article_list)
    page = ret["page"]
    ranges = ret["ranges"]
    current_page = ret["current_page"]
    user_ranking_list = Article.objects.values("user_id").annotate(s=Sum("up_count")).values_list("user__username").order_by("s")
    article_ranking_list = Article.objects.all().order_by("-up_count")
    return render(request, "index.html", locals())


@csrf_exempt
def register(request):
    """
    注册用户
    1.获取用户名、密码、邮箱、头像
    2.检验用户输入内容，错误则返回错误信息
    3.成功后如果用户上传了头像则将用户头像传入User中并创建用户
    :param request:
    :return:
    """
    user = UserForm()
    if request.method == "GET":
        return render(request, "register.html", locals())
    elif request.method == "POST":
        response = {"user": None, "msg": None}
        user = UserForm(request.POST)
        if user.is_valid():
            username = user.cleaned_data.get("username")
            response["user"] = username
            password = user.cleaned_data.get("password")
            email = user.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            print(avatar_obj)
            extra_fields = {}
            if avatar_obj:  # 如果用户上传了头像，则创建用户时将其传入，没有则传递其他填写的信息
                extra_fields["avatar"] = avatar_obj
            # 创建用户博客
            blog_obj = Blog.objects.create(title=username + "的个人博客", theme=username + ".css", site=username)
            user_obj = User.objects.create_user(username, email, password, blog_id=blog_obj.bid, **extra_fields)
        else:
            response["msg"] = user.errors

        return JsonResponse(response)


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect("/login")


@login_required
def home_site(request, username, **kwargs):
    """
    个人站点，根据用户点击的类型（分类、标签、日期）传入对应的文章列表
    :param request:
    :param username:
    :return:
    """
    user = User.objects.filter(username=username).first()
    if user:
        article_list = Article.objects.filter(user=user)
        if kwargs:
            condition = kwargs.get("condition")
            parm = kwargs.get("parm")
            if condition == "sort":
                article_list = article_list.filter(sort__title=parm)
            elif condition == "tag":
                article_list = article_list.filter(tag__name=parm)
            elif condition == "date":
                year = parm.split("-")[0]
                month = parm.split("-")[1]
                article_list = article_list.filter(create_time__year=year, create_time__month=month)
        article_list = article_list.order_by("-create_time")

        return render(request, "home_site.html", locals())
    else:
        return render(request, "404.html")


@csrf_exempt
def article(request, **kwargs):
    """
    文章详情页，根据用户名以及文章id传入用户信息、文章具体信息和评论信息
    :param request:
    :param kwargs:
    :return:
    """
    article_list = Article.objects.filter(user=request.user)
    username = kwargs.get("username")
    aid = kwargs.get("article_id")
    user = User.objects.filter(username=username).first()
    article_obj = Article.objects.filter(aid=aid).first()
    comment_list = Comment.objects.filter(article_id=article_obj.aid)

    return render(request, "article.html", locals())


@csrf_exempt
def like(request):
    """
    文章点赞
    1.获取该用户对这篇文章的操作
    2.如果用户已经对该篇文章点赞/踩过，则返回该信息
    3.如果没有则记录数据，并返回操作成功的信息
    :param request:
    :return:
    """
    is_like = request.POST.get("is_like")
    is_like = json.loads(is_like)
    user_id = request.user.uid
    article_id = request.POST.get("article_id")
    msg = None

    has_liked = Like.objects.filter(user_id=user_id, article_id=article_id).first()
    if has_liked:
        msg = "已经推荐过" if has_liked.is_like else "已经反对过"
    else:
        Like.objects.create(article_id=article_id, user_id=user_id, is_like=is_like)
        if is_like:
            # 文章的点赞数加一
            Article.objects.filter(aid=article_id).update(up_count=F("up_count") + 1)
            msg = "推荐成功"
        else:
            # 文章的反对数加一
            Article.objects.filter(aid=article_id).update(down_count=F("down_count") + 1)
            msg = "反对成功"

    return HttpResponse(msg)


@csrf_exempt
def comment(request):
    """
    文章评论
    :param request:
    :return:
    """
    content = request.POST.get("content")
    # 寻找换行符的索引，当回复评论时，第一行是艾特的对象，第二行才是评论内容
    s_index = content.find("\n")
    content = content[s_index + 1:]  # 真正的评论内容

    article_id = request.POST.get("article_id")
    parent_comment_id = request.POST.get("pid")
    user_id = request.user.uid

    with transaction.atomic():
        """
            创建事务，即评论的生成以及对应文章的评论数目加一必须是同时成功或者失败的
        """
        comment_obj = Comment.objects.create(content=content, article_id=article_id, parent_comment_id=parent_comment_id
                                             , user_id=user_id)
        Article.objects.filter(aid=article_id).update(comment_count=F("comment_count") + 1)
    response = dict()
    response["create_time"] = comment_obj.create_time
    response["username"] = request.user.username
    response["content"] = content

    return JsonResponse(response)


def is_login(request):
    data = True if request.user.is_authenticated else False
    return HttpResponse(data)


@login_required
def back_stage(request):
    """
    后台管理页面，传入分页后的文章列表
    :param request:
    :return:
    """
    article_list = Article.objects.filter(user=request.user).order_by("-create_time")
    ret = get_pages(request, article_list)
    page = ret["page"]
    ranges = ret["ranges"]
    current_page = ret["current_page"]
    return render(request, "back_stage/back_article.html", locals())


@login_required
def get_article_data(request):
    """
    当增加或者修改文章时获取用户输入的内容
    :param request:
    :return:
    """
    title = request.POST.get("title")
    content = request.POST.get("content")
    sort_id = request.POST.get("sort")
    tags = request.POST.getlist("tag")

    soup = BeautifulSoup(content, "html.parser")

    # 判断用户输入内容中是否含有scripts标签，存在就将其删除，防止xss攻击
    for tag in soup.find_all():
        if tag == "scripts":
            tag.decompose()

    abstract = soup.text[0:195]  # 用户输入的内容（不包含标签）的前194个字作为概述
    content = str(soup)
    return {"title": title, "abstract": abstract, "content": content, "sort_id": sort_id, "tags": tags}


@csrf_exempt
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    sort_list = Sort.objects.filter(blog__user=request.user)
    tag_list = Tag.objects.filter(blog__user=request.user)
    if request.method == "GET":
        return render(request, "back_stage/add_article.html", locals())
    elif request.method == 'POST':
        data = get_article_data(request)  # 获取用户输入信息
        title = data["title"]
        content = data["content"]
        sort_id = data["sort_id"]
        tags = data["tags"]
        abstract = data["abstract"]

        # 绑定事务，文章的创建以及对应标签的创建
        with transaction.atomic():
            article_obj = Article.objects.create(title=title, abstract=abstract, content=content, sort_id=sort_id,
                                                 user_id=request.user.uid)
            for i in tags:
                ArticleToTag.objects.create(article_id=article_obj.aid, tag_id=int(i))
        return redirect("/back_stage")


@csrf_exempt
def add_sort(request):
    """
    添加分类
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "back_stage/add_sort.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        blog = Blog.objects.filter(user=request.user).first()
        sort = Sort.objects.filter(title=title)
        if sort.exists():
            pass
        else:
            Sort.objects.create(title=title, blog=blog)
        return redirect("/back_stage")


@login_required
def edit_sort(request, sid):
    """
    编辑分类
    :param request:
    :param sid:
    :return:
    """
    sort = Sort.objects.filter(sid=sid).first()
    if request.method == "GET":
        return render(request, "back_stage/edit_sort.html", {"sort": sort})
    elif request.method == "POST":
        title = request.POST.get("title")
        Sort.objects.filter(sid=sid).update(title=title)
        return redirect("/back_stage")


def upload(request):
    """
    处理添加文章时用户上传的图片
    :param request:
    :return:
    """
    img = request.FILES["upload_image"]  # 富文本编辑框中设置的上传文件名
    path = os.path.join(MEDIA_ROOT, "article_image", img.name)
    # 将图片写入文件，实现上传
    with open(path, "wb") as f:
        for line in img:
            f.write(line)
    response = {
        "error": 0,
        "url": "/media/article_image/%s" % img.name
    }

    return JsonResponse(response)


@login_required
def back_stage_list(request):
    """
    后台管理界面之分类列表以及标签列表
    :param request:
    :return:
    """
    sort_list = Sort.objects.filter(blog__user=request.user)
    tag_list = Tag.objects.filter(blog__user=request.user)
    name = request.GET.get("id")
    if name == "backstage_sort":
        return render(request, "back_stage/sort_list.html", locals())
    else:
        return render(request, "back_stage/tag_list.html", locals())


@login_required
def delete(request, condition, nid):
    """
    文章/分类/标签   删除
    :param request:
    :param condition: 文章/分类/标签
    :param nid: 它们的id值
    :return:
    """
    if condition == "article":
        Article.objects.filter(aid=nid).delete()
    elif condition == "sorts":
        Sort.objects.filter(sid=nid).delete()
    elif condition == "tags":
        Tag.objects.filter(tid=nid).delete()
    return redirect("/back_stage/")


@login_required
def edit_article(request, nid):
    """
    1.进入编辑页面时，该视图函数将文章对象传递给html文件，用于html获取用户编辑之前的文章信息
    2.html将编辑后的文章信息传递给该视图函数，进行更新操作
    :param request:
    :param nid: 文章的id
    :return:
    """
    sort_list = Sort.objects.filter(blog__user=request.user)
    tag_list = Tag.objects.filter(blog__user=request.user)
    article_obj = Article.objects.filter(aid=nid).first()
    if request.method == "GET":
        return render(request, "back_stage/edit_article.html", locals())
    else:
        data = get_article_data(request)
        title = data["title"]
        content = data["content"]
        sort_id = data["sort_id"]
        tags = data["tags"]
        abstract = data["abstract"]

        with transaction.atomic():
            Article.objects.filter(aid=nid).update(title=title, abstract=abstract, content=content,
                                                   sort_id=sort_id, user_id=request.user.uid)
            article_obj.tag.clear()
            for i in tags:
                ArticleToTag.objects.create(article_id=article_obj.aid, tag_id=int(i))

        return redirect("/back_stage")


@csrf_exempt
def add_tag(request):
    """
    添加标签
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "back_stage/add_tag.html")
    elif request.method == "POST":
        name = request.POST.get("name")
        blog = Blog.objects.filter(user=request.user).first()
        tag = Tag.objects.filter(name=name)
        if tag.exists():
            pass
        else:
            Tag.objects.create(name=name, blog=blog)
        return redirect("/back_stage")


@login_required
def edit_tag(request, tid):
    """
    编辑标签
    :param request:
    :param tid:
    :return:
    """
    tag = Tag.objects.filter(tid=tid).first()
    if request.method == "GET":
        return render(request, "back_stage/edit_tag.html", {"tag": tag})
    elif request.method == "POST":
        name = request.POST.get("name")
        Tag.objects.filter(tid=tid).update(name=name)
        return redirect("/back_stage")


@csrf_exempt
@login_required
def change_password(request):
    """
    用户更改密码
    :param request:
    :return:
    """
    user = request.user
    if request.method == "GET":
        return render(request, "back_stage/change_password.html")
    elif request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        re_password = request.POST.get("re_password")
        msg = ""
        if user.check_password(old_password):
            if new_password == re_password:
                user.set_password(new_password)
                user.save()
            else:
                msg = "两次密码不一致"
        else:
            msg = "原密码错误"
        return HttpResponse(msg)


@csrf_exempt
@login_required
def change_avatar(request):
    """
    用户更改头像
    :param request:
    :return:
    """
    user = User.objects.filter(username=request.user.username).first()
    if request.method == "GET":
        return render(request, "back_stage/change_avatar.html", {"user": user})
    elif request.method == 'POST':
        avatar = request.FILES.get("avatar")
        if avatar:
            path = os.path.join(MEDIA_ROOT, "avatars", avatar.name)
            with open(path, "wb") as f:
                for line in avatar:
                    f.write(line)
            User.objects.filter(username=request.user.username).update(avatar=path)
        return HttpResponse("OK")
