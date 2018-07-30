from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from datetime import datetime
from django.core.exceptions import ValidationError
from files.models import Image
from news.models import Event

custom_error = {
    'required': '',
}


class EventForm(forms.ModelForm):
    registration_start_time = forms.TimeField(label='Påmelding start tidspunk', required=False)
    deregistration_end_time = forms.TimeField(label='Påmelding slutt tidspunk', required=False)

    event_start_time = forms.TimeField(label='Arrangement start tidspunk', required=False)
    event_end_time = forms.TimeField(label='Arrangement slutt tidspunk', required=False)

    class Meta:
        model = Event
        fields = ['title', 'main_content', 'ingress_content', 'thumbnail', 'internal', 'registration', 'max_limit', 'registration_start', 'deregistration_end', 'external_registration',
                  'time_start', 'time_end', 'place', 'place_href']


    def clean(self):
        form_data = self.cleaned_data

        # Verify max_limit
        if not form_data['max_limit']:
            form_data['max_limit'] = 0
        if form_data['max_limit'] < 0:
            if form_data['registration']:
                raise ValidationError({'max_limit': 'Antall plasser på være positivt'}, code='invalid')
            else:
                 form_data['max_limit'] = 0

        # Require date
        if not 'time_start' in form_data or not form_data['time_start']:
            raise ValidationError({'date': 'Dato er påkrevet'}, code='invalid')

        # Require registration_start_date and deregistration_end_date (if registration enabled)
        if form_data['registration']:
            if not 'registration_start' in form_data or not form_data['registration_start']:
                raise ValidationError({'registration_start': 'Påmelding start dato er påkrevet'}, code='invalid')
            if not 'deregistration_end' in form_data or not form_data['deregistration_end']:
                raise ValidationError({'deregistration_end': 'Avmelding slutt dato er påkrevet'}, code='invalid')

        # Merge start/end 'time and date
        try:
            form_data['time_start'] = datetime.combine(form_data['time_start'], form_data['event_start_time'])
        except ValueError:
            raise ValidationError({'time_start': 'Eventens start-tidspunkt eller dato er ugyldig'}, code='invalid')
        try:
            form_data['time_end'] = datetime.combine(form_data['time_end'], form_data['event_end_time'])
        except ValueError:
            raise ValidationError({'time_end': 'Eventens slutt-tidspunkt eller dato er ugyldig'}, code='invalid')

        # Merge registration time and date
        try:
            form_data['registration_start'] = datetime.combine(form_data['registration_start'], form_data['registration_start_time'])
        except (ValueError, KeyError):
            if form_data['registration']:
                raise ValidationError({'registration_start_time': 'Påmeldingens åpnings-tidspunkt eller dato er ugyldig'}, code='invalid')
            else:
                form_data['registration_start'] = datetime(2000, 1, 1, 0, 0)

        # Merge deregistration time and date
        try:
            form_data['deregistration_end'] = datetime.combine(form_data['deregistration_end'], form_data['deregistration_end_time'])
        except (ValueError, KeyError):
            if form_data['registration']:
                raise ValidationError({'deregistration_end_time': 'Avmeldingens slutt-tidspunkt eller dato er ugyldig'}, code='invalid')
            else:
                form_data['deregistration_end'] = datetime(2000, 1, 1, 0, 0)

        return form_data
