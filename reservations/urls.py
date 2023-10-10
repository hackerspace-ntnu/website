from django.urls import path

from reservations.views import QueueDetailView, QueueListView, ReservationsViewSet
from website.urls import api_router

app_name = "reservations"


api_router.register("reservations", ReservationsViewSet)


urlpatterns = [
    path("", QueueListView.as_view(), name="queue_list"),
    path("queue/<int:pk>/", QueueDetailView.as_view(), name="queue_detail"),
]
