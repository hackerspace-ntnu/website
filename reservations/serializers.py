from rest_framework import serializers
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.username')
    id = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ('start_date', 'end_date', 'start_time', 'end_time', 'user', 'parent_queue', 'comment',
                  'start', 'end', 'id')

        # Lets these fields be blank through validation. They will be set in serializer.save() (after validation).
        extra_kwargs = {'parent_queue': {'required': False}}
