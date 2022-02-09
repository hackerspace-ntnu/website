from django.urls import path

from reservations.views import QueueDetailView, QueueListView

app_name = "reservations"


urlpatterns = [
    path("", QueueListView.as_view(), name="queue_list"),
    path("queue/<int:pk>/", QueueDetailView.as_view(), name="queue_detail"),
]
