from django.conf.urls import url

from articles import views

urlpatterns = [
    url(r'^(?P<article_id>[0-9]+)/$', views.article, name='article'),
    url(r'^$', views.index, name='index'),
]
