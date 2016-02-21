from django import forms
from ckeditor.widgets import CKEditorWidget


class EventEditForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    ingress_content = forms.CharField(widget=CKEditorWidget(), label='Ingress')
    main_content = forms.CharField(widget=CKEditorWidget(), label='Article')
    time = forms.CharField(widget=forms.HiddenInput())
    date = forms.CharField(widget=forms.HiddenInput())
    place = forms.CharField(max_length=100, label='Location')
    place_href = forms.CharField(max_length=200, label='Location URL')


class ArticleEditForm(forms.Form):
    article_id = forms.IntegerField();
    ingress_content = forms.CharField(widget=CKEditorWidget(), label='Ingress')
    main_content = forms.CharField(widget=CKEditorWidget(), label='Article')
