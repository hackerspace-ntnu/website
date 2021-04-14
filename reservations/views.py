from django.views.generic import DetailView, ListView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from reservations.permissions import IsOwnerOrReadOnly
from reservations.models import Reservation, Queue
from reservations.serializers import ReservationsSerializer, RestrictedReservationSerializer
from django_filters import rest_framework as filters
from datetime import datetime

from website.models import Rule


class QueueDetailView(DetailView):
    model = Queue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Rule.objects.filter(printer_rule=True).exists():
            # Get first rule marked as printer rule
            context['printer_rule'] = Rule.objects.filter(printer_rule=True)[0]
        return context

class QueueListView(ListView):
    model = Queue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['reservation_list'] = Reservation.objects.filter(user=self.request.user, end__gte=datetime.now())
        else:
            context['reservation_list'] = None
        if Rule.objects.filter(printer_rule=True).exists():
            # Get first rule marked as printer rule
            context['printer_rule'] = Rule.objects.filter(printer_rule=True)[0]
        return context


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
        if self.request.user.has_perm('reservations.view_user_details'):
            return ReservationsSerializer
        return RestrictedReservationSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            # Kan ikke delete eller patche andre reservasjoner
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
