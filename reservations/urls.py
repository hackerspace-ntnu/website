from django.urls import path
from django.views.generic import ListView, CreateView

from reservations.models import Queue
from reservations.views import QueueDetail, ReservationViewSet

app_name = "reservations"

urlpatterns = [
        path('', ListView.as_view(model=Queue), name='queue_list'),
        path('create/', CreateView.as_view(model=Queue, fields='__all__'), name='create_queue'),
        path('queue/<int:pk>/', QueueDetail.as_view(), name='queue_detail'),
        path('testing/<int:pk>/', ReservationViewSet.as_view({'get': 'list'}), name='fullcalendar_test'),

]
