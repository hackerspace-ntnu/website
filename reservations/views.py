from datetime import datetime

from django.views.generic import DetailView, ListView
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from reservations.models import Queue, Reservation
from reservations.permissions import IsOwnerOrReadOnly
from reservations.serializers import ReservationsSerializer
from website.models import Rule


class QueueDetailView(DetailView):
    model = Queue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Rule.objects.filter(printer_rule=True).exists():
            # Get first rule marked as printer rule
            context["printer_rule"] = Rule.objects.filter(printer_rule=True)[0]
        return context


class QueueListView(ListView):
    model = Queue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["reservation_list"] = Reservation.objects.filter(
                user=self.request.user, end__gte=datetime.now()
            )
        else:
            context["reservation_list"] = None
        if Rule.objects.filter(printer_rule=True).exists():
            # Get first rule marked as printer rule
            context["printer_rule"] = Rule.objects.filter(printer_rule=True)[0]
        return context


class SearchDateFilter(filters.FilterSet):
    # filter out events that start after the end time of the search
    end = filters.IsoDateTimeFilter(field_name="start", lookup_expr="lt")

    # filter out events that end before the start time of the search
    start = filters.IsoDateTimeFilter(field_name="end", lookup_expr="gt")

    class Meta:
        model = Reservation
        fields = [
            "parent_queue",
        ]


class ReservationsViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SearchDateFilter

    def get_serializer_class(self):
        return ReservationsSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            # Kan ikke delete eller patche andre reservasjoner
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
