from django.contrib import admin
from .models import ForumProfile


class ForumProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'born_in_fifties')


admin.site.register(ForumProfile)
