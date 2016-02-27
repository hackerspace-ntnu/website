from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


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

    pub_date = models.DateTimeField('Publication date')
    thumbnail = models.OneToOneField(Thumbnail, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField()
    ingress_content = RichTextUploadingField()

    date = models.DateTimeField('Event date')
    place = models.CharField(max_length=100, verbose_name='Place', default='')
    place_href = models.CharField(max_length=200, verbose_name='Place URL', default='#')

    pub_date = models.DateTimeField('Publication date')

    thumbnail = models.OneToOneField(Thumbnail, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class Upload(models.Model):
    title = models.CharField(max_length=100, verbose_name='Filename')
    file = models.FileField(upload_to='uploads')

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'
