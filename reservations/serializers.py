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
        # Check for conflicting reservations
        # note that Fullcalendar allows reservations across multiple days, but not across multiple weeks

        # get reservations occurring across the same days as new reservation
        reservations = Reservation.objects.exclude(
            Q(start_date__gt=attrs['end_date']) | Q(end_date__lt=attrs['start_date'])
        )
        for r in reservations:
            if (r.start_time <= attrs['start_time'] <= r.end_time and r.start_date <= attrs['start_date']) \
                    or (r.start_time <= attrs['end_time'] <= r.end_time and r.end_date >= attrs['end_date']):
                raise serializers.ValidationError(
                    'New reservation is either partially or completely inside another reservation.'
                )
            if (attrs['start_time'] <= r.start_time) and (attrs['start_date'] <= r.start_date) \
                    and (attrs['end_time'] >= r.end_time) and (attrs['end_date'] >= r.end_date):
                raise serializers.ValidationError(
                    'New reservation completely envelopes another reservation'
                )

        return attrs

