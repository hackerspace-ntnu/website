from rest_framework import viewsets

from news.models import Event
from news.serializers.event import EventListSerializer, EventRetrieveSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        return EventRetrieveSerializer
