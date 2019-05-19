from django.views.generic import DetailView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from reservations.permissions import IsOwnerOrReadOnly
from reservations.models import Reservation, Queue
from reservations.serializers import ReservationsSerializer, RestrictedReservationSerializer
from django_filters import rest_framework as filters


class QueueDetailView(DetailView):
    model = Queue


class SearchDateFilter(filters.FilterSet):
    start = filters.IsoDateTimeFilter(field_name="start", lookup_expr='gt')
    end = filters.IsoDateTimeFilter(field_name="end", lookup_expr='lt')

    class Meta:
        model = Reservation
        fields = ['parent_queue', ]


class ReservationsViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SearchDateFilter

    def get_serializer_class(self):
        if self.request.user.has_perm('view_user_details'):
            return ReservationsSerializer
        return RestrictedReservationSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            # Kan ikke delete eller patche andre reservasjoner
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
