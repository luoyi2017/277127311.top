"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog.feeds import AllArticlesRssFeed

# 每一个 URL 对应着一个 Django 的视图函数
# 在视图函数中写上处理用户通过表单提交上来的数据的代码，比如验证数据的合法性并且保存数据到数据库中，那么用户的评论就被 Django 后台处理了。如果通过表单提交的数据存在错误，那么我们把错误信息返回给用户，并在前端重新渲染，并要求用户根据错误信息修正表单中不符合格式的数据，再重新提交。
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
    url(r'', include('comments.urls')),
    # 记得在顶部引入 AllPostsRssFeed
    url(r'^all/rss/$', AllArticlesRssFeed(), name='rss'),
    url(r'^search/', include('haystack.urls')),
]
