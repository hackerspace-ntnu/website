from django.urls import path
from django.views.generic import ListView, CreateView
from rest_framework.routers import SimpleRouter

from reservations.models import Queue
from reservations.views import ReservationViewSet, QueueDetailView

app_name = "reservations"

router = SimpleRouter()
router.register(r'api/(?P<pk_pq>[^/.]+)',
                ReservationViewSet,
                basename='reservation_api')
print(router.urls)
urlpatterns = [
        path('', ListView.as_view(model=Queue), name='queue_list'),
        path('create/', CreateView.as_view(model=Queue, fields='__all__'), name='create_queue'),
        path('queue/<int:pk>/', QueueDetailView.as_view(), name='queue_detail'),
]

"""
path('api/<int:pk>/', ReservationViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}),
     name='reservation_api'),
"""

urlpatterns += router.urls
