#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import template
from ..models import Article, Category

register = template.Library()

@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-created_time')[:num]

@register.simple_tag
# 归档
def archives():
    return Article.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    return Category.objects.all()






