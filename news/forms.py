from django import forms
from ckeditor.widgets import CKEditorWidget


class EventEditForm(forms.Form):
    event_id = forms.IntegerField();
    ingress_content = forms.CharField(widget=CKEditorWidget(), label='')
    main_content = forms.CharField(widget=CKEditorWidget(), label='')


class ArticleEditForm(forms.Form):
    article_id = forms.IntegerField();
    ingress_content = forms.CharField(widget=CKEditorWidget(), label='')
    main_content = forms.CharField(widget=CKEditorWidget(), label='')
