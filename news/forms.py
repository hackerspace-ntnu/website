from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from datetime import datetime
from django.core.exceptions import ValidationError
from files.models import Image

class EventEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Tittel')
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress', required=False)
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Beskrivelse', required=False)
    registration = forms.BooleanField(label="Påmelding", required=False)
    max_limit = forms.IntegerField(label="Antall", required=False)
    registration_start_time = forms.CharField(label='Påmelding start tidspunk')
    registration_start_date = forms.CharField(label='Påmelding start dato')
    deregistration_end_time = forms.CharField(label='Avmelding slutt tidspunk')
    deregistration_end_date = forms.CharField(label='Avmelding slutt dato')
    time_start = forms.CharField(label='Start klokkeslett')
    time_end = forms.CharField(label='Slutt klokkeslett')
    date = forms.CharField(label='Dato')
    place = forms.CharField(max_length=100, label='Sted', required=False)
    place_href = forms.CharField(max_length=200, label='Sted URL', required=False)
    thumbnail = forms.CharField(max_length=100, label='Miniatyrbilde', required=False)

    def clean(self):
        form_data = self.cleaned_data

        if not form_data['max_limit']:
            form_data['max_limit'] = 0
        if form_data['max_limit'] < 0:
            if form_data['registration']:
                raise ValidationError({'max_limit': 'Antall plasser på være positivt'}, code='invalid')
            else:
                 form_data['max_limit'] = 0

        try:
            form_data['time_start'] = datetime.strptime(form_data['date'] + ' ' + form_data['time_start'], '%d %B, %Y %H:%M')
        except ValueError:
            raise ValidationError({'time_start': 'Eventens start-tidspunkt eller dato er ugyldig'}, code='invalid')
        try:
            form_data['time_end'] = datetime.strptime(form_data['date'] + ' ' + form_data['time_end'], '%d %B, %Y %H:%M')
        except ValueError:
            raise ValidationError({'time_end': 'Eventens slutt-tidspunkt eller dato er ugyldig'}, code='invalid')
        del form_data['date']

        try:
            form_data['registration_start'] = datetime.strptime(form_data['registration_start_date'] + ' ' + form_data['registration_start_time'], '%d %B, %Y %H:%M')
        except ValueError:
            if form_data['registration']:
                raise ValidationError({'registration_start_time': 'Påmeldingens åpnings-tidspunkt eller dato er ugyldig'}, code='invalid')
            else:
                form_data['registration_start'] = datetime(2000, 1, 1, 0, 0)
        del form_data['registration_start_date']
        del form_data['registration_start_time']

        try:
            form_data['deregistration_end'] = datetime.strptime(form_data['deregistration_end_date'] + ' ' + form_data['deregistration_end_time'], '%d %B, %Y %H:%M')
        except ValueError:
            if form_data['registration']:
                raise ValidationError({'deregistration_end_time': 'Avmeldingens slutt-tidspunkt eller dato er ugyldig'}, code='invalid')
            else:
                form_data['deregistration_end'] = datetime(2000, 1, 1, 0, 0)
        del form_data['deregistration_end_date']
        del form_data['deregistration_end_time']

        if form_data['registration']:
            if not form_data['registration_start'] <= form_data['deregistration_end']:
                raise ValidationError({'registration_start_time': 'Ugyldige datoer, påmending må åpne før avmelding slutter'}, code='invalid')
            if not form_data['deregistration_end'] <= form_data['time_start']:
                raise ValidationError({'time_start': 'Ugyldige datoer, avmelding må slutte før eventen starter'}, code='invalid')

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
