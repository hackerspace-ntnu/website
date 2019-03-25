from rest_framework import serializers
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        name = obj.user.get_full_name()
        return name if name is not "" else obj.user.username

    class Meta:
        model = Reservation
        fields = ('start', 'end', 'user', 'id')
