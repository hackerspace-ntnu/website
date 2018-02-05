from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.all_news, name='all-news'),
    url(r'^events/$', views.all_events, name='all-events'),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article, name='article'),
    url(r'^article/(?P<article_id>[0-9]+)/edit', views.edit_article, name='edit-article'),
    url(r'^article/(?P<article_id>[0-9]+)/delete', views.delete_article, name='delete-article'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^event/(?P<event_id>[0-9]+)/edit', views.edit_event, name='edit-event'),
    url(r'^event/(?P<event_id>[0-9]+)/delete', views.delete_event, name='delete-event'),
    url(r'^event/(?P<event_id>[0-9]+)/attendees/$', views.event_attendees, name='event-attendees'),
    url(r'^upload-file/', views.upload_file, name='upload-file'),
    url(r'^upload-done/', views.upload_done, name='upload-done'),
    url(r'^register/(?P<event_id>[0-9]+)/$', views.register_on_event, name="register-on-event")
]
