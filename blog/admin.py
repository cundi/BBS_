# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Category, Entry
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    # 从类Category的title属性自动地生成slug字段
    prepopulated_fields = {'slug': ['title']}
    list_display = ('slug', 'title')


class EntryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)