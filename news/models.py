from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


class Thumbnail(models.Model):
    image = models.ImageField(upload_to="static/thumbnails")
    title = models.CharField(max_length=100, verbose_name="Title")

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField()
    ingress_content = RichTextUploadingField()

    pub_date = models.DateTimeField('Publication date', default=timezone.now)
    thumbnail = models.OneToOneField(Thumbnail, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField()
    ingress_content = RichTextUploadingField()

    time_start = models.DateTimeField('Start time')
    time_end = models.DateTimeField('End time')
    place = models.CharField(max_length=100, verbose_name='Place', default='')
    place_href = models.CharField(max_length=200, verbose_name='Place URL', default='#')

    pub_date = models.DateTimeField('Publication date', default=timezone.now)

    thumbnail = models.OneToOneField(Thumbnail, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class Upload(models.Model):
    title = models.CharField(max_length=100, verbose_name='Filename')
    time = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='uploads')
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'
