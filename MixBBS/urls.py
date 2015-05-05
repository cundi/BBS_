from django.conf.urls import include, url
from django.contrib import admin
from bb.views import index
import os

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^user/', include('accounts.urls', namespace='user')),
    url(r'^bbs/', include('bb.urls', namespace='bbs')),
    url(r'^toolbar/', include('tool_bar.urls', namespace='toolbar')),
    url(r'^media(?P<path>.*)', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static/media')}
        ),
    url(r'^static(?P<path>.*)', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')}
        ),
    url(r'^ckeditor/', include('ckeditor.urls')),
]