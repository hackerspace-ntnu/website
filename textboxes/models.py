from django.db import models


class Textbox(models.Model):
    class Meta:
        verbose_name_plural = "textboxes"

    header_text = models.CharField(max_length=100, verbose_name='Header')
    header_fontsize = models.IntegerField(default=32, verbose_name='Fontsize')
    header_color = models.CharField(max_length=7, default="#505050", verbose_name='Color', help_text='RGB-code')
    header_fontfamily = models.CharField(max_length=100, default="sans-serif", verbose_name='Font family')

    text_text = models.TextField(max_length=10000, verbose_name='Text')
    text_columns = models.IntegerField(default=1, verbose_name='Columns')
    text_fontsize = models.IntegerField(default=18, verbose_name='Fontsize')
    text_color = models.CharField(max_length=7, default="#505050", verbose_name='Color', help_text='RGB-code')
    text_fontfamily = models.CharField(max_length=100, default="sans-serif", verbose_name='Font family')

    pub_date = models.DateTimeField('Publication date')

    def __str__(self):
        return self.header_text
