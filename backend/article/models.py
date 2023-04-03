from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


class Avatar(models.Model):
    """
    文章标题图
    """
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Tag(models.Model):
    """
    文章标签
    """
    text = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.text


class Category(models.Model):
    """
    文章分类
    """
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    

class Article(models.Model):
    """
    博客文章
    """
    title = models.CharField(max_length=100)              # 标题
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )                                                     # 分类
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )                                                     # 标签
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name="articles"
    )                                                     # 作者
    body = models.TextField()                             # 正文
    created = models.DateTimeField(default=timezone.now)  # 创建时间
    updated = models.DateTimeField(auto_now=True)         # 更新时间

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)

        return md_body, md.toc
