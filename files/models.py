from django.db import models
from django.utils import timezone
from sorl.thumbnail import get_thumbnail
from django.core.files.base import ContentFile


def get_default_category():
    return FileCategory.objects.get_or_create(name='Diverse')[0].id


class FileCategory(models.Model):
    '''General purpose category for files'''
    name = models.CharField(max_length=50, unique=True, verbose_name='Kategori')

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tittel')
    time = models.DateTimeField(default=timezone.now)
    file = models.ImageField(upload_to='images')
    thumb = models.ImageField(upload_to='thumbnails', null=True)
    compressed = models.ImageField(upload_to='compressed', null=True)
    number = models.IntegerField(default=0)

    img_category = models.ForeignKey(
        FileCategory,
        default=get_default_category,
        on_delete=models.CASCADE,
        verbose_name='Kategori',
    )

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
        # Save file before creating thumbnail
        super(Image, self).save(*args, **kwargs)

        # Create a thumbnail for the image
        thumb = get_thumbnail(self.file, '300x300', crop='center', quality=70)
        self.thumb.save(thumb.name, ContentFile(thumb.read()), False)

        # Create a compressed version of the image
        compressed = get_thumbnail(self.file, str(self.file.width) + "x" + str(self.file.height), quality=70)
        self.compressed.save(compressed.name, ContentFile(compressed.read()), False)
        super(Image, self).save(*args, **kwargs)
