from django.conf import settings

from django.conf.urls import include, url

from django.conf.urls.static import static
from django.contrib import admin

from bb.views import index


urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^$', index, name='index'),
                  url(r'^user/', include('accounts.urls', namespace='user')),
                  url(r'^bb/', include('bb.urls', namespace='bb')),
                  url(r'^blog/', include('blog.urls', namespace='blog')),
                  url(r'^toolbar/', include('tool_bar.urls', namespace='toolbar')),
                  url(r'^ueditor/', include('DjangoUeditor.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
