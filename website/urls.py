from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from website.views import IndexView, AcceptTosRedirectView, AboutView

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tos/', TemplateView.as_view(template_name="website/tos.html"), name='tos'),
    path('tos/returning-user/', TemplateView.as_view(template_name="website/tos-returningls.html"), name='tos'),
    path('tos/accept/', AcceptTosRedirectView.as_view(), name='tos'),
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
    path('about/', AboutView.as_view(), name='about'),
    path('s/', include('django.contrib.flatpages.urls')),
    path('profile/', include('userprofile.urls')),
    path('internal/', include('internal.urls'))
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
