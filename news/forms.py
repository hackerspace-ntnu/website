from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class EventEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Tittel')
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress', required=False)
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Beskrivelse', required=False)
    registration = forms.BooleanField(label="Påmelding", required=False)
    max_limit = forms.IntegerField(label="Antall", required=False)
    time_start = forms.CharField(label='Start klokkeslett')
    time_end = forms.CharField(label='Slutt klokkeslett')
    date = forms.CharField(label='Dato')
    place = forms.CharField(max_length=100, label='Sted', required=False)
    place_href = forms.CharField(max_length=200, label='Sted URL', required=False)
    thumbnail = forms.CharField(max_length=100, label='Miniatyrbilde', required=False)


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
