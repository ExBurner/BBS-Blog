"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from django.views.static import serve
from blog.views import *
from blog.utils.sdk import *
from .settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录
    path('login/', login),
    # 获取验证码
    path('verify_code/', verify_code),
    # 主页
    path('index/', index),
    # 注册
    path('register/', register),
    # 注销
    path('logout/', logout),
    # 点赞
    path('like/', like),
    # 评论
    path('comment/', comment),
    # 上传头像
    path('upload/', upload),
    # 判断是否登录
    path('is_login/', is_login),
    # 后台管理
    path('back_stage/', back_stage),
    # 后台管理展现的数据列表（标签和分类）
    path('back_stage_list/', back_stage_list),
    # 增加文章
    path('add_article/', add_article),
    # 增加分类
    path('add_sort/', add_sort),
    # 增加标签
    path('add_tag/', add_tag),
    # 更改密码
    path('change_password/', change_password),
    # 更改头像
    path('change_avatar/', change_avatar),

    # 滑动验证码
    url(r'^pc-geetest/register', pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^mobile-geetest/register', pcgetcaptcha, name='mobilegetcaptcha'),
    url(r'^pc-geetest/validate$', pcvalidate, name='pcvalidate'),
    url(r'^pc-geetest/ajax_validate', pcajax_validate, name='pcajax_validate'),
    url(r'^mobile-geetest/ajax_validate', mobileajax_validate, name='mobileajax_validate'),

    # media配置
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 个人站点查询
    re_path(r'^(?P<username>\w+)/$', home_site),
    # 个人站点跳转
    re_path(r'^(?P<username>\w+)/(?P<condition>sort|tag|date)/(?P<parm>.*)/$', home_site),
    # 文章/分类/标签  删除
    re_path(r'^delete/(?P<condition>sorts|tags|article)/(?P<nid>\w+)/$', delete),
    # 编辑文章
    re_path(r'^edit_article/(?P<nid>\w+)/$', edit_article),
    # 编辑分类
    re_path(r'^edit_sort/(?P<sid>\w+)/$', edit_sort),
    # 编辑标签
    re_path(r'^edit_tag/(?P<tid>\w+)/$', edit_tag),
    # 文章页面
    re_path(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/$', article)
]
