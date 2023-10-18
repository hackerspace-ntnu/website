from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import article, event, template_views, upload

api_router = DefaultRouter()

api_router.register("articles", article.ArticleViewSet, basename="articles")
api_router.register("events", event.EventViewSet, basename="events")
api_router.register("media-uploads", upload.UploadViewSet, basename="media-uploads")

app_name = "news"
urlpatterns = [
    url(r"^$", template_views.ArticleListView.as_view(), name="all"),
    url(r"^(?P<pk>[0-9]+)/$", template_views.ArticleView.as_view(), name="details"),
    url(
        r"^(?P<pk>[0-9]+)/edit", template_views.ArticleUpdateView.as_view(), name="edit"
    ),
    url(r"^new", template_views.ArticleCreateView.as_view(), name="new"),
    url(
        r"^(?P<pk>[0-9]+)/delete",
        template_views.ArticleDeleteView.as_view(),
        name="delete",
    ),
    path("api/", include(api_router.urls)),
]
