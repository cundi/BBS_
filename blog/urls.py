# coding: utf-8
from django.conf.urls import url
from .views import entries_index, entry_detail

urlpatterns = [
    url(r'^index/$', entries_index),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', entry_detail),
]
