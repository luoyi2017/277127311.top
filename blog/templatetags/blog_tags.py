#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..models import Article, Category, Tag
from django import template
from django.db.models.aggregates import Count

# 自己定义一个模板标签，例如名为 get_recent_posts 的模板标签
# 这里我们从数据库获取文章列表的操作不是在视图函数中进行，而是在模板中通过自定义的 {% get_recent_posts %} 模板标签进行。
# 模板标签本质上就是一个 Python 函数
# 为了能够通过 {% get_recent_posts %} 的语法在模板中调用这个函数，必须按照 Django 的规定注册这个函数为模板标签
# 首先导入 template 这个模块，然后实例化了一个 template.Library 类，并将函数 get_recent_posts 装饰为 register.simple_tag。这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了。
# 注意 Django 1.9 后才支持 simple_tag 模板标签，如果你使用的 Django 版本小于 1.9，你将得到一个错误。

register = template.Library()

# 最新文章模板标签
@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-created_time')[:num]

# 归档模板标签
# dates 方法会返回一个列表，列表中的元素为文章的创建时间，精确到月份，order='DESC' 表明降序排列。
@register.simple_tag
def archives():
    return Article.objects.dates('created_time', 'month', order='DESC')

# 分类模板标签
@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    # return Category.objects.all()
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    # Category.objects.annotate 方法和 Category.objects.all 有点类似，它会返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情，在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。
    # 此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示。
    # 现在在 Category 列表中每一项都新增了一个 num_posts 属性记录该 Category 下的文章数量，我们就可以在模板中引用这个属性来显示分类下的文章数量了。
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)

# 标签云
@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)