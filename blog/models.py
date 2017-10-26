# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown
from django.utils.html import strip_tags

# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Category(models.Model):
    """
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    Django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    # 标签 Tag 也比较简单，和 Category 一样。
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=70)

    # 文章正文使用 TextField 来存储大段文本。
    body = models.TextField()

    # 这两列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 通过复写模型的 save 方法，从正文字段摘取前 N 个字符保存到摘要字段。
    # 先将 body 中的 Markdown 文本转为 HTML 文本，去掉 HTML 文本里的 HTML 标签，然后摘取文本的前 54 个字符作为摘要。去掉 HTML 标签的目的是防止前 54 个字符中存在块级 HTML 标签而使得摘要格式比较难看。可以看到很多网站都采用这样一种生成摘要的方式。
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Article, self).save(*args, **kwargs)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)

    # views 字段记录阅读量,
    # 注意 views 字段的类型为 PositiveIntegerField，该类型的值只允许为正整数或 0，因为阅读量不可能为负值。初始化时 views 的值为 0。
    views = models.PositiveIntegerField(default=0)

    # 一旦用户访问了某篇文章，这时就应该将 views 的值 +1，这个过程最好由 Article 模型自己来完成，因此再给模型添加一个自定义的方法：
    # increase_views 方法首先将自身对应的 views 字段的值 +1（此时数据库中的值还没变），然后调用 save 方法将更改后的值保存到数据库。注意这里使用了 update_fields 参数来告诉 Django 只更新数据库中 views 字段的值，以提高效率。
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    # 生成article的URL
    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        # 'blog:detail'，意思是blog应用下的name = detail的函数
        # 在blog/urls.py中通过app_name = 'blog'告诉了Django这个URL模块是属于blog应用的，因此Django能够顺利地找到blog应用下name为detail的视图函数，这里 detail 对应的规则就是 article/(?P<pk>[0-9]+)/ 这个正则表达式，如果 Article 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，那么 get_absolute_url 函数返回的就是 /article/255/ ，这样 Article 自己就生成了自己的 URL。
        return reverse('blog:detail', kwargs={'pk': self.pk})





    # 为了让文章（Post）按发布时间逆序排列，即最新发表的文章排在文章列表的最前面，我们对返回的文章列表进行了排序，即各个视图函数中都有类似于 Post.objects.all().order_by('-created_time') 这样的代码，这导致了很多重复。因为只要是返回的文章列表，基本都是逆序排列的，因此我们可以在 Post 模型中指定 Post 的自然排序方式。
    # Django 允许我们在 models.Model 的子类里定义一个 Meta 的内部类，这个内部类通过指定一些属性来规定这个类该有的一些特性，例如在这里我们要指定 Post 的排序方式。
    # 列表中可以用多个项，比如 ordering = ['-created_time', 'title'] ，那么首先依据 created_time 排序，如果 created_time 相同，则再依据 title 排序。这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序，因此可以删掉视图函数中对文章列表中返回结果进行排序的代码了。
    class Meta:
        ordering = ['-created_time']