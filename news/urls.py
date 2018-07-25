from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ArticleListView.as_view(), name='all-news'),
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^(?P<article_id>[0-9]+)/edit', views.edit_article, name='edit-article'),
    url(r'^(?P<article_id>[0-9]+)/delete', views.delete_article, name='delete-article'),
]
