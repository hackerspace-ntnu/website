from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from datetime import datetime
from django.core.exceptions import ValidationError
from files.models import Image

custom_error = {
    'required': '',
}

class EventEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Tittel')
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress', required=False)
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Beskrivelse', required=False)
    registration = forms.BooleanField(label="Påmelding", required=False)
    max_limit = forms.IntegerField(label="Antall", required=False)
    registration_start_time = forms.CharField(label='Påmelding start tidspunk', required=False)
    registration_start_date = forms.CharField(label='Påmelding start dato', required=False)
    deregistration_end_time = forms.CharField(label='Avmelding slutt tidspunk', required=False)
    deregistration_end_date = forms.CharField(label='Avmelding slutt dato', required=False)
    time_start = forms.CharField(label='Start klokkeslett')
    time_end = forms.CharField(label='Slutt klokkeslett')
    date = forms.CharField(label='Dato', error_messages=custom_error)
    place = forms.CharField(max_length=100, label='Sted', required=False)
    place_href = forms.CharField(max_length=200, label='Sted URL', required=False)
    thumbnail = forms.CharField(max_length=100, label='Miniatyrbilde', required=False)

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
        if not 'date' in form_data or not form_data['date']:
            raise ValidationError({'date': 'Dato er påkrevet'}, code='invalid')

        # Require registration_start_date and deregistration_end_date (if registration enabled)
        if form_data['registration']:
            if not 'registration_start_date' in form_data or not form_data['registration_start_date']:
                raise ValidationError({'registration_start_date': 'Påmelding start dato er påkrevet'}, code='invalid')
            if not 'deregistration_end_date' in form_data or not form_data['deregistration_end_date']:
                raise ValidationError({'deregistration_end_date': 'Avmelding slutt dato er påkrevet'}, code='invalid')

        # Merge start/end 'time and date
        try:
            form_data['time_start'] = datetime.strptime(form_data['date'] + ' ' + form_data['time_start'], '%d %B, %Y %H:%M')
        except ValueError:
            raise ValidationError({'time_start': 'Eventens start-tidspunkt eller dato er ugyldig'}, code='invalid')
        try:
            form_data['time_end'] = datetime.strptime(form_data['date'] + ' ' + form_data['time_end'], '%d %B, %Y %H:%M')
        except ValueError:
            raise ValidationError({'time_end': 'Eventens slutt-tidspunkt eller dato er ugyldig'}, code='invalid')
        if 'date' in form_data: del form_data['date']

        # Merge registration time and date
        try:
            form_data['registration_start'] = datetime.strptime(form_data['registration_start_date'] + ' ' + form_data['registration_start_time'], '%d %B, %Y %H:%M')
        except (ValueError, KeyError):
            if form_data['registration']:
                raise ValidationError({'registration_start_time': 'Påmeldingens åpnings-tidspunkt eller dato er ugyldig'}, code='invalid')
            else:
                form_data['registration_start'] = datetime(2000, 1, 1, 0, 0)
        if 'registration_start_date' in form_data: del form_data['registration_start_date']
        if 'registration_start_time' in form_data: del form_data['registration_start_time']

        # Merge deregistration time and date
        try:
            form_data['deregistration_end'] = datetime.strptime(form_data['deregistration_end_date'] + ' ' + form_data['deregistration_end_time'], '%d %B, %Y %H:%M')
        except (ValueError, KeyError):
            if form_data['registration']:
                raise ValidationError({'deregistration_end_time': 'Avmeldingens slutt-tidspunkt eller dato er ugyldig'}, code='invalid')
            else:
                form_data['deregistration_end'] = datetime(2000, 1, 1, 0, 0)
        if 'deregistration_end_date' in form_data: del form_data['deregistration_end_date']
        if 'deregistration_end_time' in form_data: del form_data['deregistration_end_time']

        # Verify dates
        if form_data['registration']:
            if not form_data['registration_start'] <= form_data['deregistration_end']:
                raise ValidationError({'registration_start_time': 'Ugyldige datoer, påmending må åpne før avmelding slutter'}, code='invalid')
            if not form_data['deregistration_end'] <= form_data['time_start']:
                raise ValidationError({'time_start': 'Ugyldige datoer, avmelding må slutte før eventen starter'}, code='invalid')

        # Verify thumbnail
        try:
            form_data['thumbnail'] = Image.objects.get(id=int(form_data['thumbnail']))
        except (TypeError, ValueError, Image.DoesNotExist):
            form_data['thumbnail'] = None

        return form_data

class ArticleEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Tittel')
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress', required=False)
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Artikkel', required=False)
    thumbnail = forms.CharField(max_length=100, label='Miniatyrbilde', required=False)


class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class EventRegistrationForm(forms.Form):
    user = forms.CharField(max_length=50)
    event = forms.CharField(max_length=50)


class AttendeeForm(forms.Form):
    user = forms.CharField(label='Name', max_length=100)
