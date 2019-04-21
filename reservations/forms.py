from django import forms

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['comment', 'start_date', 'end_date', 'start_time', 'end_time']

        labels = {
            'comment': 'Kommentar',
            'start_date': 'Startdato',
            'end_date': 'Sluttdato',
            'start_time': 'Starttid',
            'end_time': 'Sluttid',
        }

        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'start_time': forms.TimeInput(attrs={'class': 'timepicker'}),
            'end_time': forms.TimeInput(attrs={'class': 'timepicker'}),
        }
