from django.urls import path
from django.views.generic import ListView

from reservations.models import Queue
from reservations.views import QueueDetailView


app_name = "reservations"


urlpatterns = [
        path('', ListView.as_view(model=Queue), name='queue_list'),
        path('queue/<int:pk>/', QueueDetailView.as_view(), name='queue_detail')
]
