from django.urls import path

from . import views
from .ical import HSEventFeed, HSEventSingleFeed

app_name = "events"
urlpatterns = [
    path("", views.EventListView.as_view(), name="all"),
    path("<int:pk>/", views.EventView.as_view(), name="details"),
    path("<int:pk>/edit/", views.EventUpdateView.as_view(), name="edit"),
    path("<int:pk>/attended/", views.EventAttendeeEditView.as_view(), name="attended"),
    path("new", views.EventCreateView.as_view(), name="new"),
    path("<int:pk>/delete/", views.EventDeleteView.as_view(), name="delete"),
    path("<int:event_id>/register/", views.register_on_event, name="register"),
    path("feed.ics", HSEventFeed()),
    path("<int:pk>/feed.ics", HSEventSingleFeed()),
]
