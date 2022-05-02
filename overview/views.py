from datetime import datetime

from django.utils import timezone
from django.views.generic import TemplateView

from news.models import Article, Event
from watchlist.models import ShiftSlot
from website.models import Rule

WEEKDAYS = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]


class OverviewView(TemplateView):
    template_name = "overview/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the 5 events closest to starting
        event_list = list(
            Event.objects.filter(
                time_start__gt=timezone.now(),
                draft=False,
                internal=False,
            ).order_by("time_start")[:5]
        )

        # Add expired events if we couldn't fill the 5 slots
        if len(event_list) < 5:
            to_fill = 5 - len(event_list)
            expired_events = Event.objects.filter(
                time_start__lte=timezone.now(),
                internal=False,
                draft=False,
            ).order_by("-time_start")[:to_fill]
            event_list += list(expired_events)

        current_time = datetime.now()

        # Get five published articles
        article_list = Article.objects.filter(draft=False, internal=False).order_by(
            "-pub_date"
        )[:5]

        # Get shifts from today
        valid_shifts = ShiftSlot.objects.filter(
            weekday=current_time.weekday()
        ).order_by("start")

        shift_dict = {}
        for shift in valid_shifts:
            row_header = "{} -\n{}".format(
                shift.start.strftime("%H:%M"), shift.end.strftime("%H:%M")
            )
            shift_dict[row_header] = shift

        context = {
            "article_list": article_list,
            "event_list": event_list,
            "current_time": current_time,
            "shifts": shift_dict,
            "today": current_time.weekday(),
            "weekday": WEEKDAYS[current_time.weekday()],
            "rule": Rule.objects.filter(id=9).first(),
        }

        return context
