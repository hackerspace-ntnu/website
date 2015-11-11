from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^$', views.index, name='index'),
]
