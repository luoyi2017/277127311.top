from django.db import models
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    # auto_now_add 的作用是，当评论数据保存到数据库时，自动把 created_time 的值指定为当前时间。created_time 记录用户发表评论的时间，我们肯定不希望用户在发表评论时还得自己手动填写评论发表时间，这个时间应该自动生成。
    created_time = models.DateTimeField(auto_now_add=True)
    # 这个评论关联到某篇文章
    article = models.ForeignKey('blog.Article')

    def __str__(self):
        return self.text[:20]