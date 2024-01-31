from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from news.filters.event import EventFilter
from news.models import Event
from news.serializers.event import EventListSerializer, EventRetrieveSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventListSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = EventFilter
    search_fields = ["title", "ingress_content", "main_content"]

    def get_queryset(self):
        queryset = Event.objects.all()
        user = self.request.user

        include_internal = user and user.has_perm("news.can_view_internal_event")
        if include_internal:
            queryset = Event.objects.all()
        else:
            queryset = Event.objects.filter(internal=False)
        return queryset.order_by("-pub_date")

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        return EventRetrieveSerializer
