from django.urls import path

from . import views

app_name = "projectarchive"
urlpatterns = [
    path("", views.ArticleListView.as_view(), name="all"),
    path("<int:pk>", views.ArticleView.as_view(), name="details"),
    path("new", views.ArticleCreateView.as_view(), name="create"),
    path("<int:pk>/edit", views.ArticleUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete", views.ArticleDeleteView.as_view(), name="delete"),
]
