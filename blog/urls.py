#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

# 通过 app_name='blog' 告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间。
# 一些第三方应用中也可能有叫 index、detail 的视图函数，那么怎么把它们区分开来，防止冲突呢？方法就是通过 app_name 来指定命名空间
# 如果忘了在 blog\urls.py 中添加这一句，接下来可能会得到一个 NoMatchReversed 异常。
app_name = 'blog'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # 对 url 函数来说，第二个参数传入的值必须是一个函数。而 IndexView 是一个类，不能直接替代 index 函数。好在将类视图转换成函数视图非常简单，只需调用类视图的 as_view() 方法即可
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 视图函数的调用就是这个样子：detail(request, pk=?)。
    # 我们这里必须从 URL 里捕获文章的 id，因为只有这样我们才能知道用户访问的究竟是哪篇文章。
    # 详情页：
    # url(r'^article/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
    # 归档页：两个括号括起来的地方是两个命名组参数，Django 会从用户访问的 URL 中自动提取这两个参数的值，然后传递给其对应的视图函数。例如如果用户想查看 2017 年 3 月下的全部文章，他访问 /archives/2017/3/，那么 archives 视图函数的实际调用为：archives(request, year=2017, month=3)。
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    # url(r'^search/$', views.search, name='search'),
]



