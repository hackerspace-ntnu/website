import datetime

from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationView(APIView):
    @staticmethod
    def _parse_datetime_str(datetime_str):
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

    def get(self, request, **kwargs):
        try:
            start = self._parse_datetime_str(request.GET['start'])
            end = self._parse_datetime_str(request.GET['end'])
            # Q() lets you combine queries
            queryset = Reservation.objects.filter(
                Q(parent_queue_id=kwargs['pk']) &
                Q(start__gte=start) &
                Q(end__lte=end)
            )
        except MultiValueDictKeyError:
            queryset = Reservation.objects.all()

        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    @staticmethod
    def _parse_datetime_str(datetime_str):
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

    def get_queryset(self):
        try:
            start = self._parse_datetime_str(self.request.GET['start'])
            end = self._parse_datetime_str(self.request.GET['end'])
            # Q() lets you combine queries
            queryset = Reservation.objects.filter(
                Q(parent_queue_id=self.kwargs['pk']) &
                Q(start__gte=start) &
                Q(end__lte=end)
            )
            return queryset
        except MultiValueDictKeyError:
            qs = Reservation.objects.all()
            print(qs)
            return qs

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
