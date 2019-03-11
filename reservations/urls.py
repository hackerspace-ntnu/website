from django.urls import path

from reservations.views import QueueDetail, ReservationViewSet

app_name = "reservations"

urlpatterns = [
        path('queue/<int:pk>/', QueueDetail.as_view(), name='queue_detail'),
        path('testing/<int:pk>/', ReservationViewSet.as_view({'get': 'list'}), name='fullcalendar_test'),

]
