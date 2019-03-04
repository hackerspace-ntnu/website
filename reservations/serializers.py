from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from reservations.models import Reservation


class ReservationSerializer(serializers.Serializer):
    class Meta:
        model = Reservation
        fields = ('start', 'end')


class ReservationViewSet(ViewSet):

    def list(self, request, pk):
        print('\n\n asdasdas \n\n')
        print(self, request.GET)
        queryset = Reservation.objects.filter(parent_queue_id=pk)
        print(queryset)
        serializer = ReservationSerializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data)
