from rest_framework import viewsets

from watchlist.models import ShiftSlot
from watchlist.serializers.shift_slot import ShiftSlotSerializer


class ShiftSlotViewSet(viewsets.ModelViewSet):
    queryset = ShiftSlot.objects.all()
    serializer_class = ShiftSlotSerializer
