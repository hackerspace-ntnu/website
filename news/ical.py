from django.urls import reverse
from django_ical.views import ICalFeed

from .models import Event


class HSEventFeed(ICalFeed):
    """
    ICal feed for Hackerspace events
    """

    product_id = "-//hackerspace-ntnu.no//Hackerspace//NB"
    timezone = "UTC+01:00"
    link = "/events/"
    file_name = "hackerspace.ics"

    def get_object(self, request):
        return {
            "internal_access": request.user.has_perm("news.can_view_internal_event")
        }

    def items(self, attrs):
        events = Event.objects.all().order_by("-time_start")
        if not attrs["internal_access"]:
            events = events.filter(internal=False)
        return events

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.ingress_content

    def item_start_datetime(self, item):
        return item.time_start

    def item_end_datetime(self, item):
        return item.time_end

    def item_link(self, item):
        return reverse("events:details", kwargs={"pk": item.pk})

    def item_location(self, item):
        return item.place

    def item_organizer(self, item):
        if not item.responsible:
            return ""
        return f"{item.responsible.first_name} {item.responsible.last_name}"


class HSEventSingleFeed(HSEventFeed):
    """
    Feed for a single event
    """

    def get_object(self, request, pk=None):
        attrs = super().get_object(request)
        attrs["id"] = pk
        return attrs

    def items(self, attrs):
        items = super().items(attrs)
        return items.filter(pk=attrs["id"])

    def file_name(self, attrs):
        items = self.items(attrs)
        if not items:
            return "error_contact_devops.ics"
        title = items[0].title
        return f"{title}.ics"
