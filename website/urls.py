from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.views.static import serve as static_serve

from website.views import index, test, calendar, about, set_cookie

admin.autodiscover()

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^news/', include('news.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^authentication/', include('authentication.urls')),
    url(r'^opptak/', include('applications.urls')),
    url(r'^door/', include('door.urls')),
    url(r'^ckeditor_uploader/', include('ckeditor_uploader.urls')),
    url(r'^opptak/', include('applications.urls'), name='opptak'),
    url(r'^test/$', test, name="500-test"),
    url(r'^files/', include('files.urls')),
    url(r'^inventory/', include('inventory.urls'), name='inventory'),
    url(r'^groups/', include('committees.urls', namespace='verv')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^rpi/', include('rpi.urls')),
    url(r'^kalender/', calendar, name='calendar'),
    url(r'^about/$', about, name='about'),
    url(r'^s/', include('django.contrib.flatpages.urls')),
    url(r'^members/', include('userprofile.urls')),
    url(r'^user/', include('userprofile.urls')),
    url(r'^vaktliste/', include('vaktliste.urls', namespace='vaktliste')),
    url(r'^feide/', include('authentication_feide.urls')),
    url(r'^kaffi/', include('koohii.urls')),
    url(r'^ajax/setcookie', set_cookie, name='set_cookie')
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
    from website.views import handler404

    urlpatterns += [
        url(r'test404', handler404, name='404')
    ]
