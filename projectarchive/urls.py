from django.urls import path
from . import views

app_name = 'projectarchive'
urlpatterns = [
    path(r'', views.ArticleListView.as_view(), name='Article_List'),
    path('<int:pk>', views.ArticleView.as_view(), name='details'),
    path(r'new', views.ArticleCreateView.as_view(), name='Article_Create'),
    path('<int:pk>/edit', views.ArticleUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', views.ArticleDeleteView.as_view(), name='delete'),
]




