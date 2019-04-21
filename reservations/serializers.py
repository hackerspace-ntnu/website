from django.db.models import Q
from rest_framework import serializers
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.username')
    id = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ('start_date', 'end_date', 'start_time', 'end_time', 'user', 'parent_queue', 'comment',
                  'start', 'end', 'id')

        # Let these fields be blank through validation. They will be set in serializer.save() (after validation).
        extra_kwargs = {'parent_queue': {'required': False}}

    def validate(self, attrs):
        # Fullcalendar allows reservations across multiple days
        print(attrs)
        # get all reservations that cross dates with the new reservations
        reservations = Reservation.objects.exclude(Q(start_date__gt=attrs['end_date']) | Q(end_date__lt=attrs['start_date']))
        print(reservations)
        for r in reservations:
            # check if the new reservation is either:
            # 1. completely inside another reservation
            if r.start_time <= attrs['start_time'] and r.end_time >= attrs['end_time']:
                print('1')
            # 2. partially inside another reservation, either at the end or at the start
            if r.start_time <= attrs['start_time'] <= r.end_time or r.start_time <= attrs['end_time'] <= r.end_time:
                print('2')
            # 3. completely envelopes another reservation
            if attrs['start_time'] <= r.start_time and attrs['end_time'] >= r.end_time:
                print('3')

        return attrs

