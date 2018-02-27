from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CommitteeEditForm(forms.Form):
    header = forms.CharField(max_length=100, label='Overskrift')
    one_liner = forms.CharField(widget=CKEditorUploadingWidget(), label='Lynbeskrivelse', required=False)
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Beskrivelse', required=False)
    thumbnail = forms.CharField(max_length=100, label='Bilde', required=False)
    visible = forms.BooleanField(label="Synlig", required=False)


class CommitteeCreateForm(forms.Form):

    name = forms.CharField(max_length=100, label='Gruppenavn')

    def __init__(self, *args, **kwargs):
        try:
            self.parent_committee = kwargs.pop('parent_committee')
        except KeyError:
            pass
        super().__init__(*args, **kwargs)

    def clean(self):
        try:
            name = self.cleaned_data['name']
        except KeyError:
            raise ValidationError({'name': _("This field is required.")}, code='invalid')

        # All names for sibling committees must be unique.
        sibling_names = list(map(str.lower, self.parent_committee.subcommittees.values_list('name', flat=True)))
        if name.lower() in sibling_names:
            raise ValidationError({'name': _("The name is not unique for the parent committee.")}, code='invalid')
