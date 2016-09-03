from django import forms

class ImageUpload(forms.Form):
    title = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=100, required=False)
    file = forms.FileField()

class ImageEdit(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=100, required=False)
    file = forms.FileField(required=False)

class ImageSearch(forms.Form):
    search = forms.CharField(max_length=100)
