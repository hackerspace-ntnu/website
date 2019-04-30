from django.db import models
from django.utils import timezone
from sorl.thumbnail import get_thumbnail
from django.core.files.base import ContentFile

class Image(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(max_length=100, blank=True, verbose_name='Description')
    tags = models.CharField(max_length=100, verbose_name='Tags')
    time = models.DateTimeField(default=timezone.now)
    file = models.ImageField(upload_to='images')
    thumb = models.ImageField(upload_to='thumbnails', null=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        if self.number > 1:
            return self.title + ' (' + str(self.number) + ')'
        return self.title

    def url(self):
        return '/media/' + str(self.file)

    def abs_url(self):
        return 'https://www.hackerspace-ntnu.no/media/' + str(self.file)

    def thumb_url(self):
        if not self.thumb:
            self.save()

        return '/media/' + str(self.thumb)

    def save(self, *args, **kwargs):
        # Create a thumbnail for the image
        # Save file before creating thumbnail
        super(Image, self).save(*args, **kwargs)
        thumb = get_thumbnail(self.file, '300x300', crop='center', quality=99)
        self.thumb.save(thumb.name, ContentFile(thumb.read()), False)
        # Save again with thumbnail
        super(Image, self).save(*args, **kwargs)
