from django.urls import path

from .ical import HSEventFeed, HSEventSingleFeed
from .views import template_views

app_name = "events"
urlpatterns = [
    path("", template_views.EventListView.as_view(), name="all"),
    path("<int:pk>/", template_views.EventView.as_view(), name="details"),
    path("<int:pk>/edit/", template_views.EventUpdateView.as_view(), name="edit"),
    path(
        "<int:pk>/attended/",
        template_views.EventAttendeeEditView.as_view(),
        name="attended",
    ),
    path(
        "<int:pk>/skills/",
        template_views.EventAttendeeSkillsView.as_view(),
        name="skills",
    ),
    path("new", template_views.EventCreateView.as_view(), name="new"),
    path("<int:pk>/delete/", template_views.EventDeleteView.as_view(), name="delete"),
    path("<int:event_id>/register/", template_views.register_on_event, name="register"),
    path("feed.ics", HSEventFeed()),
    path("<int:pk>/feed.ics", HSEventSingleFeed()),
]
