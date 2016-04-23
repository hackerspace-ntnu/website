from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.http.response import HttpResponse
from django.views.static import serve as static_serve
from website.views import index

admin.autodiscover()

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt', lambda _: HttpResponse('User-agent: *\nDisallow: /')),
    url(r'^news/', include('news.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^authentication/', include('authentication.urls')),
    url(r'^door/', include('door.urls')),
    url(r'^ckeditor_uploader/', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_notify_pattern
urlpatterns += [
    url(r'^notify/', get_notify_pattern()),
    url(r'^wiki/', get_wiki_pattern())
]


if settings.DEBUG:
    from website.views import test404, test500
    urlpatterns += [
        url(r'test404', test404, name='404'),
        url(r'test500', test500, name='500')
    ]