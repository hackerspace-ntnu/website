from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name='all'),
    url(r'^(?P<pk>[0-9]+)/$', views.EventView.as_view(), name='details'),
    url(r'^(?P<pk>[0-9]+)/edit', views.EventUpdateView.as_view(), name='edit'),
    url(r'^new', views.EventCreateView.as_view(), name='new'),
    url(r'^(?P<pk>[0-9]+)/delete', views.EventDeleteView.as_view(), name='delete'),
    url(r'^(?P<event_id>[0-9]+)/register', views.register_on_event, name="register")
]
