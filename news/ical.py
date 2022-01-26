from django_ical.views import ICalFeed
from .models import Event
from django.urls import reverse

class EventFeed(ICalFeed):
    """
    A simple event calender
    """

    product_id = '-//hackerspace-ntnu.no//Hackerspace//NB'
    timezone = 'UTC+01:00'
    link = '/events/'
    file_name = 'hackerspace.ics'

    def get_object(self, request):
        return {
            'internal_access': request.user.has_perm('news.can_view_internal_event')
        }

    def items(self, attrs):
        events = Event.objects.all().order_by('-time_start')
        if not attrs['internal_access']:
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
        return reverse('events:details', kwargs={'pk': item.pk})
