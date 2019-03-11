import datetime

from django.db.models import Q
from django.views.generic import DetailView
from rest_framework.viewsets import ModelViewSet

from reservations.models import Queue, Reservation
from reservations.serializers import ReservationSerializer


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    model = Reservation

    @staticmethod
    def _parse_datetime_str(datetime_str):
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

    def get_queryset(self):
        start = self._parse_datetime_str(self.request.GET['start'])
        end = self._parse_datetime_str(self.request.GET['end'])
        queryset = Reservation.objects.filter(
            Q(parent_queue_id=self.kwargs['pk']) &
            Q(start__gte=start) &
            Q(end__lte=end)
        )
        print(queryset)
        return queryset


class QueueDetail(DetailView):
    model = Queue





