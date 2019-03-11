from rest_framework import serializers
from reservations.models import Reservation


class ReservationSerializer(serializers.Serializer):

    class Meta:
        model = Reservation
        fields = ('start', 'end')
