from django import forms


class ItemsUploadForm(forms.Form):
    file = forms.FileField(label="Legg ved fil", required=True)
