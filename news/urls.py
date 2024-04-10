from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("", views.ArticleListView.as_view(), name="all"),
    path("<int:pk>/", views.ArticleView.as_view(), name="details"),
    path("<int:pk>/edit/", views.ArticleUpdateView.as_view(), name="edit"),
    path("new/", views.ArticleCreateView.as_view(), name="new"),
    path("<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="delete"),
]
