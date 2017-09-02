import markdown
from django.shortcuts import render, get_object_or_404
# 引入 Category 类
from .models import Article, Category
from comments.forms import CommentForm
# Create your views here.

def index(request):
    # article_list = Article.objects.all().order_by('-created_time')
    article_list = Article.objects.all()
    return render(request, 'blog/index.html', context={'article_list': article_list})

def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # 记得在顶部引入 markdown 模块
    article.body = markdown.markdown(article.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 article 下的全部评论
    comment_list = article.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'article': article,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)

# 归档、存档
def archives(request, year, month):
    # article_list = Article.objects.filter(created_time__year=year,
    #                                 created_time__month=month
    #                                 ).order_by('-created_time')
    article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'article_list': article_list})

# 分类
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    # article_list = Article.objects.filter(category=cate).order_by('-created_time')
    article_list = Article.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'article_list': article_list})
















