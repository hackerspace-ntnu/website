from rest_framework import serializers

from watchlist.models import ShiftSlot


class ShiftSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftSlot
        fields = "__all__"
