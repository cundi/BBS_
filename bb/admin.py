from django.contrib import admin
from bb.models import Category, Forum, Topic, Post, Appendix, Notification


class CategoryAdmin(admin.ModelAdmin):
    pass


class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}



admin.site.register(Category,)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post,)
admin.site.register(Appendix)
admin.site.register(Notification)