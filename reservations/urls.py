from django.urls import path
from django.views.generic import ListView, CreateView, DetailView

from reservations.models import Queue
from reservations.views import ReservationViewSet, ReservationView

app_name = "reservations"

urlpatterns = [
        path('', ListView.as_view(model=Queue), name='queue_list'),
        path('create/', CreateView.as_view(model=Queue, fields='__all__'), name='create_queue'),
        path('queue/<int:pk>/', DetailView.as_view(model=Queue), name='queue_detail'),
        path('testing/<int:pk>/', ReservationView.as_view(), name='testing'),
]
