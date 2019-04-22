import datetime

from django.db.models import Q
from rest_framework import serializers

from authentication.templatetags.check_user_group import has_group
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.username')
    id = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ('start_date', 'end_date', 'start_time', 'end_time', 'user', 'parent_queue', 'comment',
                  'start', 'end', 'id')

    def validate(self, attrs):
        # disallow reservations into the past, but be slightly forgiving
        now = datetime.datetime.now() - datetime.timedelta(minutes=15)
        if attrs['start_date'] < now.date() \
                or (attrs['start_date'] == now.date() and attrs['start_time'] < now.time()):
            raise serializers.ValidationError("Invalid timeframe. Reservations into past are disallowed")

        # disallow weekend and late/early hour reservations to non-members
        user = self.context['request'].user
        if not has_group(user, 'member') and not user.is_superuser:
            if attrs['start_time'].hour < 10 or attrs['end_time'].hour > 18 \
                    or attrs['start_date'].weekday() >= 6 or attrs['end_date'].weekday() >= 6:
                raise serializers.ValidationError(
                    "Non-members are not allowed to make reservations outside opening hours"
                )

        # Check if the new reservation conflicts with any of the old ones in the same queue
        # note that Fullcalendar allows reservations across multiple days, but not across multiple weeks
        reservations = Reservation.objects\
            .filter(parent_queue_id=attrs['parent_queue'])\
            .exclude(Q(start_date__gt=attrs['end_date']) | Q(end_date__lt=attrs['start_date']))
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

