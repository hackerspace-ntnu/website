from django.db.models.fields import forms
from django.utils.translation import gettext_lazy as _

from news.forms import SplitDateTimeFieldCustom


class InterviewEmailForm(forms.Form):
    location = forms.CharField(
        label=_("Plassering"),
        max_length=100,
        required=True,
    )
    location_link = forms.CharField(
        label=_("Lenke til plassering"),
        max_length=100,
        required=False,
    )
    start_time = SplitDateTimeFieldCustom(
        label=_("Starttidspunkt"),
        required=True,
    )
    end_time = SplitDateTimeFieldCustom(
        label=_("Sluttidspunkt"),
        required=False,
    )
