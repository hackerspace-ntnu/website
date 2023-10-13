from django.conf.urls import url

from .views import template_views

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
]
