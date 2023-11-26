from django.db.models.fields import forms
from django.utils.translation import gettext_lazy as _


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
    start_time = forms.DateTimeField(
        label=_("Tidspunkt"),
        required=True,
    )
    end_time = forms.DateTimeField(
        label=_("Sluttidspunkt"),
        required=False,
    )
