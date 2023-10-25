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
        queryset = Event.objects.all().order_by("-pub_date")
        user = self.request.user
        non_drafts = queryset.filter(draft=False)

        if user.is_authenticated:
            return non_drafts.union(queryset.filter(author=user, draft=True))
        return non_drafts

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        return EventRetrieveSerializer
