from django import forms

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    """
    Reservations use datetime fields to track start and end,
    but we show separate time and date fields to the user.
    """
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time', 'class': 'timepicker'}),
        label='Starttid'
    )
    end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time', 'class': 'timepicker'}),
        label='Sluttid'
    )
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'datepicker'}),
        label='Startdato'
    )
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'datepicker'}),
        label='Sluttdato'
    )

    class Meta:
        model = Reservation
        fields = ['comment']

        labels = {
            'comment': 'Kommentar',
        }
