from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reservations.views import QueueDetailView, QueueListView, ReservationsViewSet

api_router = DefaultRouter()

api_router.register("reservations", ReservationsViewSet, basename="reservations")

app_name = "reservations"

urlpatterns = [
    path("", QueueListView.as_view(), name="queue_list"),
    path("queue/<int:pk>/", QueueDetailView.as_view(), name="queue_detail"),
    path("api/", include(api_router.urls)),
]
