from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.all_news, name='all-news'),
    url(r'^(?P<article_id>[0-9]+)/$', views.article, name='article'),
    url(r'^(?P<article_id>[0-9]+)/edit', views.edit_article, name='edit-article'),
    url(r'^(?P<article_id>[0-9]+)/delete', views.delete_article, name='delete-article'),
]
