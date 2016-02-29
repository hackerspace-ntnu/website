from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class EventEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress')
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Article')
    time_start = forms.CharField(widget=forms.HiddenInput())
    time_end = forms.CharField(widget=forms.HiddenInput())
    date = forms.CharField(widget=forms.HiddenInput())
    place = forms.CharField(max_length=100, label='Location')
    place_href = forms.CharField(max_length=200, label='Location URL')


class ArticleEditForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    article_id = forms.IntegerField(widget=forms.HiddenInput());
    ingress_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Ingress')
    main_content = forms.CharField(widget=CKEditorUploadingWidget(), label='Article')


class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
