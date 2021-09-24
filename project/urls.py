from django.conf.urls import url

from . import views

app_name = 'archive'
urlpatterns = [

    # Stemmer dette?...
    url(r'archive', views.EventListView.as_view(), name='all'),
    url(r'archive/<int:pk>', views.EventView.as_view(), name='all'),
    url(r'archive/new', views.EventCreateView.as_view(), name='all'),

    url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='details'),
    url(r'^(?P<pk>[0-9]+)/edit', views.ArticleUpdateView.as_view(), name='edit'),
    url(r'^new', views.ArticleCreateView.as_view(), name='new'),
    url(r'^(?P<pk>[0-9]+)/delete', views.ArticleDeleteView.as_view(), name='delete'),
]




