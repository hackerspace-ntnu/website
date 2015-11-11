from django.db import models


class Thumbnail(models.Model):
    thumbnail_image = models.ImageField(upload_to="static/thumbnails")
    #thumbnail_src = models.CharField(max_length=200, verbose_name="Source", help_text="http://example.com/image.jpg")
    thumbnail_title = models.CharField(max_length=100, verbose_name="Title")

    def __str__(self):
        return self.thumbnail_title


class Article(models.Model):
    header_text = models.CharField(max_length=100, verbose_name='Header')
    header_fontsize = models.IntegerField(default=32, verbose_name='Fontsize')
    header_color = models.CharField(max_length=7, default="#000000", verbose_name='Color', help_text='RGB-code')
    header_fontfamily = models.CharField(max_length=100, default="sans-serif", verbose_name='Font family')

    text_text = models.TextField(max_length=10000, verbose_name='Text')
    text_fontsize = models.IntegerField(default=14, verbose_name='Fontsize')
    text_color = models.CharField(max_length=7, default="#000000", verbose_name='Color', help_text='RGB-code')
    text_fontfamily = models.CharField(max_length=100, default="sans-serif", verbose_name='Font family')

    ingress_text = models.TextField(max_length=500, verbose_name='Text')
    ingress_fontsize = models.IntegerField(default=18, verbose_name='Fontsize')
    ingress_color = models.CharField(max_length=7, default="#505050", verbose_name='Color', help_text='RGB-code')
    ingress_fontfamily = models.CharField(max_length=100, default="sans-serif", verbose_name='Font family')

    ingress_header_text = models.CharField(max_length=100, verbose_name='Header')
    ingress_header_fontsize = models.IntegerField(default=24, verbose_name='Fontsize')
    ingress_header_color = models.CharField(max_length=7, default="#505050", verbose_name='Color', help_text='RGB-code')
    ingress_header_fontfamily = models.CharField(max_length=100, default="sans-serif", verbose_name='Font family')

    pub_date = models.DateTimeField('Publication date')

    thumbnail = models.OneToOneField(Thumbnail, null=True)

    post_type = models.IntegerField(choices=((0, "Article"), (1, "Event")), default=0, null=False, blank=False)

    def __str__(self):
        return self.header_text


class Image(models.Model):
    # image = models.ImageField(upload_to="img")
    article = models.ForeignKey(Article)
    image_src = models.CharField(max_length=200, verbose_name="Source", help_text="http://example.com/image.jpg")
    image_title = models.CharField(max_length=100, verbose_name="Title")
    image_customDimensions = models.BooleanField(default=False, verbose_name="Custom dimensions",
                                                 help_text="Uncheck if you want the original dimensions.")
    image_width = models.IntegerField(default=200, verbose_name="Width")
    image_height = models.IntegerField(default=200, verbose_name='Height')
    image_float = models.CharField(max_length=10, default="Left", choices=[('Left', 'Left'), ('Right', 'Right')],
                                   verbose_name='Float')

    def __str__(self):
        return self.image_title
