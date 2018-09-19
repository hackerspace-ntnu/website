from django.urls import path

from reservations.views import QueueListView, QueueDetailView, QueueCreateView, QueueUpdateView, QueueDeleteView

app_name = "reservations"

urlpatterns = [
    path('', QueueListView.as_view(), name='queue_list'),
    path('create', QueueCreateView.as_view(), name="queue_create"),
    path('<int:pk>', QueueDetailView.as_view(), name='queue_detail'),
    path('<int:pk>/update', QueueUpdateView.as_view(), name='queue_update'),
    path('<int:pk>/delete', QueueDeleteView.as_view(), name='queue_delete'),
]
