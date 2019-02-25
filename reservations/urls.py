from django.urls import path

from reservations.views import QueueListView, QueueDetailView, QueueCreateView, QueueUpdateView, QueueDeleteView, \
    ReservationUpdateView, ReservationDeleteView, ReservationCreateView

app_name = "reservations"

urlpatterns = [
    path('', QueueListView.as_view(), name='queue_list'),
    path('queue/create', QueueCreateView.as_view(), name="queue_create"),
    path('queue/<int:pk>/update', QueueUpdateView.as_view(), name='queue_update'),
    path('queue/<int:pk>/delete', QueueDeleteView.as_view(), name='queue_delete'),

    path('queue/<int:pk>/reserve', ReservationCreateView.as_view(), name="reservation_create"),
    path('queue/<int:pk>/', QueueDetailView.as_view(), name='queue_detail'),
    path('<int:pk>/update', ReservationUpdateView.as_view(), name='reservation_update'),
    path('<int:pk>/delete', ReservationDeleteView.as_view(), name='reservation_delete'),
]
