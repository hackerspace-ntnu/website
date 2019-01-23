from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_notify_pattern

from website.views import IndexView, AcceptTosRedirectView

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('showcase', TemplateView.as_view(template_name="website/showcase.html"), name='showcase'),
    path('tos/', TemplateView.as_view(template_name="website/tos.html"), name='tos'),
    path('tos/returning-user/', TemplateView.as_view(template_name="website/tos-returningls.html"), name='tos'),
    path('tos/accept/', AcceptTosRedirectView.as_view(), name='tos'),
    path('showcase/vr/', TemplateView.as_view(template_name="website/vr.html"), name='vr'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='website/robots.txt',
                                             content_type='text/plain')),
    path('news/', include('news.urls')),
    path('events/', include('news.event_urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('authentication/', include('authentication.urls', namespace='auth')),
    path('door/', include('door.urls')),
    path('opptak/', include('applications.urls'), name='opptak'),
    path('files/', include('files.urls')),
    # url(r'^inventory/', include('inventory.urls'), name='inventory'),
    path('groups/', include('committees.urls', namespace='verv')),
    path('chaining/', include('smart_selects.urls')),
    path('kalender/', TemplateView.as_view(template_name="website/calendar.html"), name='calendar'),
    path('about/', TemplateView.as_view(template_name="website/about.html"), name='about'),
    path('s/', include('django.contrib.flatpages.urls')),
    path('profile/', include('userprofile.urls')),
    path('feide/', include('authentication_feide.urls')),
    path('kaffe/', include('kaffe.urls')),
    path('internal/', include('internal.urls'))
]
# Add wiki and notify urls
urlpatterns += [
    path('notify/', get_notify_pattern()),
    path('wiki/', get_wiki_pattern())
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
