# # coding: utf-8
# from django.conf.urls import url
#
# from bb.views import (index, topic_view, create_topic, create_topic_reply, edit_topic,
#                           delete_topic, preview, category_details, forum_view, forum_list, forum_topics, search,
#                           forums_topics, delete_topic_reply, pre_create_topic, category_all, add_appendix,
# )
#
#
# urlpatterns = [
#     url(r'^$', index, name='index'),
#     url(r'^category/all/$', category_all, name='category_all'),
#     url(r'^category/(?P<category_id>\d+)/$', category_details, name='category_details'),
#     url(r'^forum/list/$', forum_list, name='forum_list'),
#     url(r'^forum/(?P<forum_id>\d+)/$', forum_view, name='forum_view'),
#     url(r'^forums/topics/$', forums_topics, name='forums_topics'),
#     url(r'^pre_create_topic/$', pre_create_topic, name='pre_create_topic'),
#     url(r'^forum/(?P<forum_id>\d+)/create_topic/$', create_topic, name='create_topic'),
#     url(r'^forum/(?P<forum_id>\d+)/topic_all/$', forum_topics, name='forum_topic_all'),
#     url(r'^topic/(?P<topic_id>\d+)/$', topic_view, name='topic_view'),
#     url(r'^topic/(?P<topic_id>\d+)/reply/$', create_topic_reply, name='create_topic_reply'),
#     url(r'^topic/(?P<topic_id>\d+)/edit/$', edit_topic, name='edit_topic'),
#     url(r'^topic(?P<topic_id>\d+)/delete/$', delete_topic, name='delete_topic'),
#     url(r'^topic/(?P<topic_id>\d+)/appendix/$', add_appendix, name='add_appendix'),
#     url(r'^post/(?P<post_id>\d+)/delete/$', delete_topic_reply, name='delete_topic_reply'),
#     url(r'^search(?P<kw>.*?)/$', search, name='search'),
#     url(r'^preview/$', preview, name='preview'),
# ]