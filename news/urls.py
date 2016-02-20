from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    #url(r'^event/$', views.events, name='events'),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article, name='article'),
    #url(r'^article/$', views.articles, name='articles'),
]
