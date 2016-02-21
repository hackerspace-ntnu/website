from django import forms
from ckeditor.widgets import CKEditorWidget


class EventEditForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    ingress_content = forms.CharField(widget=CKEditorWidget(), label='')
    main_content = forms.CharField(widget=CKEditorWidget(), label='')
    time = forms.CharField(widget=forms.HiddenInput())
    date = forms.CharField(widget=forms.HiddenInput())


class ArticleEditForm(forms.Form):
    article_id = forms.IntegerField();
    ingress_content = forms.CharField(widget=CKEditorWidget(), label='')
    main_content = forms.CharField(widget=CKEditorWidget(), label='')
