# -*- coding: utf-8 -*-
from django.db import models
from uuslug import uuslug


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