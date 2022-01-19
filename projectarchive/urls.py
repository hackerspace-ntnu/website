from django.urls import path
from . import views

app_name = 'projectarchive'
urlpatterns = [
    path(r'', views.ArticleListView.as_view(), name='Article_List'),
    path('<int:pk>', views.ArticleView.as_view(), name='Article_View'),
    path(r'new', views.ArticleCreateView.as_view(), name='Article_Create'),

    path('<int:pk>/edit', views.ArticleUpdateView.as_view(), name='edit'),
    # path('detail/<int:pk>/edit', views.ProjectUpdateView.as_view(), name='edit'),

    # path('detail/<int:pk>/edit', views.ArticleDeleteView.as_view(), name='delete'),

]

# urlpatterns = [
#     url(r'^$', views.ArticleListView.as_view(), name='all'),
#     url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='details'),
#     url(r'^(?P<pk>[0-9]+)/edit', views.ArticleUpdateView.as_view(), name='edit'),
#     url(r'^new', views.ArticleCreateView.as_view(), name='new'),
#     url(r'^(?P<pk>[0-9]+)/delete', views.ArticleDeleteView.as_view(), name='delete'),
# ]



