from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class EventEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress', required=False)
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Article', required=False)
    time_start = forms.CharField(widget=forms.HiddenInput())
    time_end = forms.CharField(widget=forms.HiddenInput())
    date = forms.CharField(widget=forms.HiddenInput())
    place = forms.CharField(max_length=100, label='Location', required=False)
    place_href = forms.CharField(max_length=200, label='Location URL', required=False)
    thumbnail = forms.CharField(max_length=100, label='Thumbnail', required=False)


class ArticleEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    article_id = forms.IntegerField(widget=forms.HiddenInput())
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress', required=False)
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Article', required=False)
    thumbnail = forms.CharField(max_length=100, label='Thumbnail', required=False)


class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
