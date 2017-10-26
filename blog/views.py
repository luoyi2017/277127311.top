#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Tag
from comments.forms import CommentForm
import markdown
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q

# 将 index 视图函数改写为类视图：
# 这里 IndexView 的功能是从数据库中获取文章（Post）列表，ListView 就是从数据库中获取某个模型列表数据的，所以 IndexView 继承 ListView。
# 通过一些属性来指定这个视图函数需要做的事情。这里我们指定了三个属性。
# model。将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
# template_name。指定这个视图渲染的模板。
# context_object_name。指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
# index 视图函数首先通过 Post.objects.all() 从数据库中获取文章（Post）列表数据，并将其保存到 post_list 变量中。而在类视图中这个过程 ListView 已经帮我们做了。我们只需告诉 ListView 去数据库获取的模型是 Post，而不是 Comment 或者其它什么模型，即指定 model = Post。将获得的模型数据列表保存到 post_list 里，即指定 context_object_name = 'post_list'。然后渲染 blog/index.html 模板文件，index 视图函数中使用 render 函数。但这个过程 ListView 已经帮我们做了，我们只需指定渲染哪个模板即可。
# 类视图 ListView 已经帮我们写好了分页逻辑，我们只需通过指定 paginate_by 属性来开启分页功能即可，即在类视图中指定 paginate_by 属性的值
class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 5

    # 以下待看
    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context


    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data



# def index(request):
#     # all方法返回的是一个QuerySet（可以理解成一个类似于列表的数据结构）
#     # created_time，即文章的创建时间。- 号表示逆序，如果不加 - 则是正序。
#     # article_list = Article.objects.all().order_by('-created_time')
#     # 在 models.py的Article 类的内部定义了一个 Meta 类，并指定默认排序属性为逆序，所以这边不用再排序了
#     article_list = Article.objects.all()
#     return render(request, 'blog/index.html', context={'article_list': article_list})


# 将detail函数改为类函数，比较复杂，以后再看
# 记得在顶部导入 DetailView
class ArticleDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        article = super(ArticleDetailView, self).get_object(queryset=None)
        article.body = markdown.markdown(article.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        # md = markdown.Markdown(extensions=[
        #     'markdown.extensions.extra',
        #     'markdown.extensions.codehilite',
        #     'markdown.extensions.toc',
        #     # TocExtension 在实例化时其 slugify 参数可以接受一个函数作为参数，这个函数将被用于处理标题的锚点值。
        #     # Markdown 内置的处理方法不能处理中文标题，所以我们使用了 django.utils.text 中的 slugify 方法，该方法可以很好地处理中文。
        #     TocExtension(slugify=slugify),
        # ])
        # article.body = md.convert(article.body)
        # article.toc = md.toc
        return article

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context



# # 详情页
# def detail(request, pk):
#     # 视图函数根据从 URL 捕获的文章 id（也就是 pk，这里 pk 和 id 是等价的）获取数据库中文章 id 为该值的记录，然后传递给模板。
#     # 从 django.shortcuts 模块导入的 get_object_or_404 方法，其作用就是当传入的 pk 对应的 Article 在数据库存在时，就返回对应的 article，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
#     article = get_object_or_404(Article, pk=pk)
#
#     # 当用户请求访问某篇文章时，处理该请求的视图函数为 detail 。一旦该视图函数被调用，说明文章被访问了一次
#     # 只需在视图函数中调用模型的 increase_views 方法即可。
#     article.increase_views()
#
#     # 记得在顶部引入 markdown 模块，以下将 Markdown 格式的文本渲染成 HTML 文本
#     # 额外的参数extensions是对 Markdown 语法的拓展，这里使用了三个拓展，分别是 extra、codehilite、toc。
#     # extra 本身包含很多拓展，而 codehilite 是语法高亮拓展，这为我们后面的实现代码高亮功能提供基础，而 toc 则允许我们自动生成目录。
#     # 使用 codehilite 拓展，只是实现代码高亮的第一步，还需要需要安装 Pygments。
#     # Pygments的原理是把代码切分成一个个单词，然后为这些单词添加css样式，不同的词应用不同的样式，这样就实现了代码颜色的区分，即高亮了语法。
#     # 还需引入一个样式文件来给这些被添加了样式的单词定义颜色。
#     # 在项目的 blog\static\blog\css\highlights\ 目录下应该能看到很多 .css 样式文件，这些文件是用来提供代码高亮样式的。选择一个你喜欢的样式文件，在 base.html 引入即可（别忘了使用 static 模板标签）。
#     article.body = markdown.markdown(article.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     # 记得在顶部导入 CommentForm
#     form = CommentForm()
#     # 获取这篇 article 下的全部评论
#     comment_list = article.comment_set.all()
#     # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
#     context = {'article': article,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'blog/detail.html', context=context)


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,created_time__month=month)


# # 归档
# def archives(request, year, month):
#     # Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表，所以 Django 要求我们把点替换成了两个下划线，即 created_time__year。
#     article_list = Article.objects.filter(created_time__year=year,
#                                         created_time__month=month
#                                           )
#                                     # ).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'article_list': article_list})


# 将 category 视图函数改写为类视图
# 和 IndexView 不同的地方是，覆写了父类的 get_queryset 方法。该方法默认获取指定模型的全部列表数据。为了获取指定分类下的文章列表数据，覆写该方法，改变它的默认行为。
# 首先是需要根据从 URL 中捕获的分类 id（也就是 pk）获取分类，这和 category 视图函数中的过程是一样的。不过注意一点的是，在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，非命名组参数值保存在实例的 args 属性（是一个列表）里。所以我们使了 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。然后我们调用父类的 get_queryset 方法获得全部文章列表，紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。
# 可以看到 CategoryView 类中指定的属性值和 IndexView 中是一模一样的，所以如果为了进一步节省代码，甚至可以直接继承 IndexView：
# class CategoryView(ListView):
class CategoryView(IndexView):
    # model = Article
    # template_name = 'blog/index.html'
    # context_object_name = 'article_list'
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

# # 分类
# # 首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类。
# def category(request, pk):
#     # 记得在开始部分导入 Category 类
#     cate = get_object_or_404(Category, pk=pk)
#     # article_list = Article.objects.filter(category=cate).order_by('-created_time')
#     article_list = Article.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'article_list': article_list})


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    # 校验，如果用户没有输入搜索关键词而提交了表单，我们就无需执行查询，我们就在模板中渲染一个错误提示信息。
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    # 过滤条件是 title__icontains=q，即 title 中包含（contains）关键字 q，前缀 i 表示不区分大小写。这里 icontains 是查询表达式（Field lookups），我们在之前也使用过其他类似的查询表达式，其用法是在模型需要筛选的属性后面跟上两个下划线。
    # 从 from django.db.models 中引入了一个新的东西：Q 对象。Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑。例如这里 Q(title__icontains=q) | Q(body__icontains=q) 表示标题（title）含有关键词 q 或者正文（body）含有关键词 q ，或逻辑使用 | 符号。如果不用 Q 对象，就只能写成 title__icontains=q, body__icontains=q，这就变成标题（title）含有关键词 q 且正文（body）含有关键词 q，就达不到我们想要的目的。
    article_list = Article.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'article_list': article_list})



