from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from rest_framework import routers

from inventory.views.item import InventoryListAPIView
from reservations import views as reservation_views
from search.views import SearchAPIView, SearchView, UserSearchAPIView
from userprofile.views import (
    MembersAPIView,
    MembersView,
    MostRecentTermsOfServiceView,
    TermsOfServiceCreateView,
    TermsOfServiceView,
)
from website.views import (
    AboutView,
    AcceptTosRedirectView,
    AcceptTosView,
    AdminView,
    IndexView,
    RuleDetailsView,
    RulesView,
)

handler404 = "website.views.handler404"
handler403 = "website.views.handler403"
handler500 = "website.views.handler500"

# Add rest framework urls
router = routers.DefaultRouter()
router.register(r"reservations", reservation_views.ReservationsViewSet)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="website/robots.txt", content_type="text/plain"
        ),
    ),
    path("tos/", MostRecentTermsOfServiceView.as_view(), name="tos"),
    path("tos/returning-user/", AcceptTosView.as_view(), name="tos-returningls"),
    path("tos/accept/", AcceptTosRedirectView.as_view(), name="tos-accept"),
    path("tos/create/", TermsOfServiceCreateView.as_view(), name="tos-create"),
    path(
        "tos/create/<int:pk>/", TermsOfServiceCreateView.as_view(), name="tos-create-id"
    ),
    path("tos/<int:pk>/", TermsOfServiceView.as_view(), name="tos-details"),
    path("news/", include("news.urls")),
    path("events/", include("news.event_urls")),
    path("authentication/", include("authentication.urls", namespace="auth")),
    path("door/", include("door.urls")),
    path("opptak/", include("applications.urls"), name="opptak"),
    path("files/", include("files.urls")),
    path("about/", AboutView.as_view(), name="about"),
    path("rules/", RulesView.as_view(), name="rules"),
    path("rules/<int:pk>/", RuleDetailsView.as_view(), name="rule_details"),
    path("s/", include("django.contrib.flatpages.urls")),
    path("search/", SearchView.as_view(), name="search"),
    path("api/search/", SearchAPIView.as_view(), name="search-api"),
    path("api/user-search/", UserSearchAPIView.as_view(), name="user-search-api"),
    path("profile/", include("userprofile.urls")),
    path("reservations/", include("reservations.urls"), name="reservations"),
    path("members/", MembersView.as_view(), name="member-list"),
    path("api/members/", MembersAPIView.as_view(), name="members-api"),
    path("admin-panel/", AdminView.as_view(), name="admin"),
    path("feide/", include("social_django.urls", namespace="social")),
    path("api/", include(router.urls)),
    path(
        "api/inventory/",
        InventoryListAPIView.as_view(),
        name="inventory-api",
    ),
    path("inventory/", include("inventory.urls")),
    path("vaktliste/", include("watchlist.urls")),
    path("internalportal/", include("internalportal.urls")),
    path("projectarchive/", include("projectarchive.urls"), name="projectarchive"),
    path("markdownx/", include("markdownx.urls")),
]

admin.site.site_header = "Adminpanel for Viktige Folk"
admin.site.site_title = "Admin hackerspace-ntnu.no"
admin.site.index_title = "Vennligst ikke ødelegg noe"
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            static_serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]
    admin.site.index_title = "Velkommen tilbake, Mester"
