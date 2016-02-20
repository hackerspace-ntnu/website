from django.db import models
from ckeditor.fields import RichTextField
from django import forms
from ckeditor.widgets import CKEditorWidget


class Thumbnail(models.Model):
    image = models.ImageField(upload_to="static/thumbnails")
    title = models.CharField(max_length=100, verbose_name="Title")

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextField()
    ingress_content = RichTextField()

    pub_date = models.DateTimeField('Publication date')
    thumbnail = models.OneToOneField(Thumbnail, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextField()
    ingress_content = RichTextField()

    date = models.DateTimeField('Event date')
    place = models.CharField(max_length=100, verbose_name='Place', default='')
    place_href = models.CharField(max_length=200, verbose_name='Place URL', default='#')

    pub_date = models.DateTimeField('Publication date')

    thumbnail = models.OneToOneField(Thumbnail, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class EventEditForm(forms.Form):
    event_id = forms.IntegerField();
    ingress_content = forms.CharField(widget = CKEditorWidget(), label='')
    main_content = forms.CharField(widget = CKEditorWidget(), label='')


class ArticleEditForm(forms.Form):
    article_id = forms.IntegerField();
    ingress_content = forms.CharField(widget = CKEditorWidget(), label='')
    main_content = forms.CharField(widget = CKEditorWidget(), label='')
