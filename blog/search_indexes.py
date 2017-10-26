#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from haystack import indexes
from .models import Article

# django haystack 的规定。要相对某个 app 下的数据进行全文检索，就要在该 app 下创建一个 search_indexes.py 文件，然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Article），并且继承 SearchIndex 和 Indexable。
# 每个索引里面必须有且只能有一个字段为 document=True，这代表 django haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)。注意，如果使用一个字段设置了document=True，则一般约定此字段名为text，这是在 SearchIndex 类里面一贯的命名，以防止后台混乱
# 并且，haystack 提供了use_template=True 在 text 字段中，这样就允许我们使用数据模板去建立搜索引擎索引的文件，说得通俗点就是索引里面需要存放一些什么东西，例如 Post 的 title 字段，这样我们可以通过 title 内容来检索 Post 数据了。举个例子，假如你搜索 Python ，那么就可以检索出 title 中含有 Python 的Post了
# 数据模板的路径为 templates/search/indexes/youapp/\<model_name>_text.txt（例如 templates/search/indexes/blog/post_text.txt）
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()



