# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from .views import user_signup, user_login, user_logout,reset_pwd, user_info, pwd_change_done, pwd_change, pwd_reset_done


urlpatterns = patterns('',
                       url(r'signup/$', user_signup, name='sign_up'),
                       url(r'login/$', user_login, name='sign_in'),
                       url(r'logout/$', user_logout, name='logout'),
                       url(r'password_change/$', pwd_change, name='pwd_change'),
                       url(r'password_change/done/$', pwd_change_done,name='pwd_change_done'),
                       url(r'password_reset/$', reset_pwd, name='pwd_reset'),
                       url(r'password_reset/done/$', pwd_reset_done, name='pwd_reset_done'),
                       url(r'^(?P<username>\w+)_info/$', user_info, name='user_info'),
                       )