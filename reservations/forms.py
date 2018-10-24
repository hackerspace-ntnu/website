import datetime
from django.forms import ModelForm, ValidationError
from django.shortcuts import get_object_or_404
from reservations.models import Queue, Reservation


class QueueForm(ModelForm):

    class Meta:
        model = Queue
        fields = '__all__'


class ReservationForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ('date', 'start_time', 'end_time', )

    def __init__(self, *args, **kwargs):
        self.queue_id = kwargs.pop('pk')
        super().__init__(*args, **kwargs)

    def clean(self):
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)
        date = self.cleaned_data.get('date', None)
        pk = self.queue_id
        queue = get_object_or_404(Queue, pk=pk)

        if start_time > end_time:
            raise ValidationError("Invalid argument parameters")

        if date < datetime.date.today():
            raise ValidationError("You cannot make reservations back in time")

        for interval in [(r.start_time, r.end_time) for r in queue.reservations.filter(date=date)]:
            reservation_overlap = interval[1] < start_time, end_time < interval[2]
            if reservation_overlap.__contains__(True):
                raise ValidationError("Incompatible with existing reservations")
