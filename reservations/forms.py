from django import forms

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    """
    def __init__(self, *args, **kwargs):
        parent_queue = kwargs.pop('parent_queue')
        super().__init__(*args, **kwargs)
        self.fields['parent_queue'] = forms.HiddenInput()
        self.fields['parent_queue'].initial = parent_queue
    """

    class Meta:
        model = Reservation
        fields = ['comment', 'start_date', 'end_date', 'start_time', 'end_time']  # 'parent_queue'

        labels = {
            'comment': 'Kommentar',
            'start_date': 'Startdato',
            'end_date': 'Sluttdato',
            'start_time': 'Starttid',
            'end_time': 'Sluttid',
        }
