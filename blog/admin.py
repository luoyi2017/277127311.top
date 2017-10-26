from django.contrib import admin
from .models import Article, Category, Tag

# 定制 Admin
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


# 在后台注册我们自己创建的几个模型，这样 Django Admin 才能知道它们的存在
# 把新增的 ArticleAdmin 也注册进来
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)