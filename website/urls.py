from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from website.views import IndexView, AcceptTosRedirectView, AboutView, AdminView, AcceptTosView, RulesView, \
    RuleDetailsView
from userprofile.views import TermsOfServiceCreateView, TermsOfServiceView, MostRecentTermsOfServiceView
from userprofile.views import ProfileListView
from django.contrib.auth.decorators import permission_required
from ckeditor_uploader import views as ck_upload_views
from rest_framework import routers
from reservations import views as reservation_views
from inventory import views as inventory_views

handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'

# Add rest framework urls
router = routers.DefaultRouter()
router.register(r'reservations', reservation_views.ReservationsViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='website/robots.txt', content_type='text/plain')),
    path('tos/', MostRecentTermsOfServiceView.as_view(), name='tos'),
    path('tos/returning-user/', AcceptTosView.as_view(), name='tos-returningls'),
    path('tos/accept/', AcceptTosRedirectView.as_view(), name='tos-accept'),
    path('tos/create/', TermsOfServiceCreateView.as_view(), name='tos-create'),
    path('tos/create/<int:pk>/', TermsOfServiceCreateView.as_view(), name='tos-create-id'),
    path('tos/<int:pk>/', TermsOfServiceView.as_view(), name='tos-details'),
    path('news/', include('news.urls')),
    path('events/', include('news.event_urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload', permission_required('news.add_article')(ck_upload_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse', permission_required('news.add_article')(ck_upload_views.browse), name='ckeditor_browse'),
    path('authentication/', include('authentication.urls', namespace='auth')),
    path('door/', include('door.urls')),
    path('opptak/', include('applications.urls'), name='opptak'),
    path('files/', include('files.urls')),
    path('about/', AboutView.as_view(), name='about'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('rules/<int:pk>/', RuleDetailsView.as_view(), name='rule_details'),
    path('s/', include('django.contrib.flatpages.urls')),
    path('profile/', include('userprofile.urls')),
    path('reservations/', include('reservations.urls')),
    path('members/', ProfileListView.as_view(), name='member-list'),
    path('admin-panel/', AdminView.as_view(), name='admin'),
    path('feide/', include('social_django.urls', namespace='social')),
    path('api/', include(router.urls)),
    path('api/inventory/', inventory_views.InventoryListAPIView.as_view(), name='inventory-api'),
    path('inventory/', include('inventory.urls')),
    path('vaktliste/', include('watchlist.urls'))
]

admin.site.site_header = "Adminpanel for Viktige Folk"
admin.site.site_title = "Admin hackerspace-ntnu.no"
admin.site.index_title = "Vennligst ikke ødelegg noe"
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve,
                {'document_root': settings.MEDIA_ROOT}),
    ]
    admin.site.index_title = "Velkommen tilbake, Mester"
