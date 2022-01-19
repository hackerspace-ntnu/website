from django.urls import path

from . import views

app_name = 'project'
urlpatterns = [
    path(r'', views.ProjectListView.as_view(), name='Project_List'),
    path('<int:pk>', views.ProjectView.as_view(), name='Project_View'),
    # path('detail/<int:pk>', views.ProjectView.as_view(), name='Project_View'),
    path(r'new', views.ProjectCreateView.as_view(), name='Project_Create'),

    path('<int:pk>/edit', views.ProjectUpdateView.as_view(), name='edit'),
    # path('detail/<int:pk>/edit', views.ProjectUpdateView.as_view(), name='edit'),

    # path('detail/<int:pk>/edit', views.ArticleDeleteView.as_view(), name='delete'),



]




