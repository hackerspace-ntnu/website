from django_filters import FilterSet

from news.models import Event


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ("draft",)
