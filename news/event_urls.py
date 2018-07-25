from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name='all-events'),
    url(r'^(?P<pk>[0-9]+)/$', views.EventView.as_view(), name='event'),
    url(r'^(?P<event_id>[0-9]+)/edit', views.edit_event, name='edit-event'),
    url(r'^new', views.NewEvent, name='new-event'),
    url(r'^(?P<event_id>[0-9]+)/delete', views.delete_event, name='delete-event'),
    url(r'^(?P<event_id>[0-9]+)/attendees/$', views.event_attendees, name='event-attendees'),
    url(r'^register/(?P<event_id>[0-9]+)/$', views.register_on_event, name="register-on-event")
]
