from dal import autocomplete
from .models import Committee

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CommitteeEditForm(forms.Form):
    header = forms.CharField(max_length=100, label='Overskrift')
    one_liner = forms.CharField(widget=CKEditorUploadingWidget(), label='Lynbeskrivelse', required=False)
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Beskrivelse', required=False)
    image = forms.CharField(max_length=100, label='Bilde', required=False)
