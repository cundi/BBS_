# -*- coding: utf-8 -*-
from django.db import models
from uuslug import uuslug
from django.core.urlresolvers import reverse
from accounts.models import BlogProfile
from DjangoUeditor.models import UEditorField

LIVE_STATUS = 1
DRAFT_STATUS = 2
HIDDEN_STATUS = 3

STATUS_CHOICES = (
    (LIVE_STATUS, '发布'),
    (DRAFT_STATUS, '草稿'),
    (HIDDEN_STATUS, '隐藏'),
)


class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, help_text="推荐从title自动生成值，且唯一", blank=True)        # url路径中Category实例的的别名
    description = models.TextField()

    class Meta:
        ordering = ['title']                # 按照Category实例的title属性的值从a-z排列这些值
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    # 通过使用uuslug函数处理类的实例和实例的title属性，最后调用Category的超类的save方法
    def save(self, *args, **kwargs):
            self.slug = uuslug(self.title, instance=self)
            super(Category, self).save(*args, **kwargs)

    # 显示实例的slug格式的URL
    def get_absolute_url(self):
        return reverse('blog:categories_details', args=[self.slug])


class Entry(models.Model):
    title = models.CharField(max_length=250)
    body = UEditorField()
    pub_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(BlogProfile)
    enable_comments = models.BooleanField(default=True)
    slug = models.SlugField(unique_for_date='pub_date')     # 生成类似2015/06/06/entry-title/这样的URL部分
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    featured = models.BooleanField(default=False)           # 对发布的文章标记“精华”

    categories = models.ManyToManyField(Category)
    tags = models.CharField(help_text="使用空格分隔标签")

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:entry', args=[self.pub_date.strftime("%Y/%b/%d"), self.slug])
