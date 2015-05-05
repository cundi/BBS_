# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from .views import user_signup, user_login, user_logout,reset_pwd, user_info


urlpatterns = patterns('',
                       url(r'signup/$', user_signup, name='sign_up'),
                       url(r'login/$', user_login, name='sign_in'),
                       url(r'logout/$', user_logout, name='logout'),
                       url(r'pwd_reset/$', reset_pwd, name='pwd_reset'),
                       url(r'^(?P<username>\w+)_info/$', user_info, name='user_info'),
                       )