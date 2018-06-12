from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.views.static import serve as static_serve
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_notify_pattern

from website.views import index, test, calendar, about, showcase, virtualreality

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^showcase/$', showcase, name='showcase'),
    url(r'^showcase/vr/', virtualreality, name='vr'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt', TemplateView.as_view(template_name='robots.txt',
                                             content_type='text/plain')),
    url(r'^news/', include('news.urls')),
    url(r'^events/', include('news.event_urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^authentication/', include('authentication.urls')),
    url(r'^door/', include('door.urls')),
    url(r'^opptak/', include('applications.urls'), name='opptak'),
    url(r'^files/', include('files.urls')),
    # url(r'^inventory/', include('inventory.urls'), name='inventory'),
    url(r'^groups/', include('committees.urls', namespace='verv')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^rpi/', include('rpi.urls')),
    url(r'^kalender/', calendar, name='calendar'),
    url(r'^about/', about, name='about'),
    url(r'^s/', include('django.contrib.flatpages.urls')),
    url(r'^profile/', include('userprofile.urls')),
    url(r'^users/', include('vaktliste.urls', namespace='vaktliste')),
    url(r'^feide/', include('authentication_feide.urls')),
    url(r'^kaffe/', include('kaffe.urls')),
]
# Add wiki and notify urls
urlpatterns += [
    url(r'^notify/', get_notify_pattern()),
    url(r'^wiki/', get_wiki_pattern())
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static_serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
