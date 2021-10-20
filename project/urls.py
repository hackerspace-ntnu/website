from django.conf.urls import url

from . import views

app_name = 'project'
urlpatterns = [
    # url(r'archive', views.ProjectListView.as_view(), name='Project_List'),
    # url(r'archive/<int:pk>', views.ProjectView.as_view(), name='Project_View'),
    # url(r'archive/new', views.ProjectCreateView.as_view(), name='Project_Create'),

    url(r'', views.ProjectListView.as_view(), name='Project_List'),
    url('/detail/   <int:pk>', views.ProjectView.as_view(), name='Project_View'),
    # url(r'^(?P<pk>[0-9]+)/$', views.ProjectView.as_view(), name='Project_View'),
    url(r'/new', views.ProjectCreateView.as_view(), name='Project_Create'),




]




