from django.forms import ModelForm, ValidationError

from reservations.models import Queue


class QueueForm(ModelForm):

    class Meta:
        model = Queue
        fields = '__all__'

    def clean(self):
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)

        if start_time > end_time:
            raise ValidationError("Your queue must start before it can end")
