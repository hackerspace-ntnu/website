# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('header_text', models.CharField(verbose_name='Header', max_length=100)),
                ('header_fontsize', models.IntegerField(verbose_name='Fontsize', default=32)),
                ('header_color', models.CharField(verbose_name='Color', default='#000000', max_length=7, help_text='RGB-code')),
                ('header_fontfamily', models.CharField(verbose_name='Font family', default='sans-serif', max_length=100)),
                ('text_text', models.TextField(verbose_name='Text', max_length=10000)),
                ('text_fontsize', models.IntegerField(verbose_name='Fontsize', default=14)),
                ('text_color', models.CharField(verbose_name='Color', default='#000000', max_length=7, help_text='RGB-code')),
                ('text_fontfamily', models.CharField(verbose_name='Font family', default='sans-serif', max_length=100)),
                ('ingress_text', models.TextField(verbose_name='Text', max_length=500)),
                ('ingress_fontsize', models.IntegerField(verbose_name='Fontsize', default=18)),
                ('ingress_color', models.CharField(verbose_name='Color', default='#505050', max_length=7, help_text='RGB-code')),
                ('ingress_fontfamily', models.CharField(verbose_name='Font family', default='sans-serif', max_length=100)),
                ('ingress_header_text', models.CharField(verbose_name='Header', max_length=100)),
                ('ingress_header_fontsize', models.IntegerField(verbose_name='Fontsize', default=24)),
                ('ingress_header_color', models.CharField(verbose_name='Color', default='#505050', max_length=7, help_text='RGB-code')),
                ('ingress_header_fontfamily', models.CharField(verbose_name='Font family', default='sans-serif', max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='Publication date')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('image_src', models.CharField(verbose_name='Source', max_length=200, help_text='http://example.com/image.jpg')),
                ('image_title', models.CharField(verbose_name='Title', max_length=100)),
                ('image_customDimensions', models.BooleanField(verbose_name='Custom dimensions', default=False, help_text='Uncheck if you want the original dimensions.')),
                ('image_width', models.IntegerField(verbose_name='Width', default=200)),
                ('image_height', models.IntegerField(verbose_name='Height', default=200)),
                ('image_float', models.CharField(verbose_name='Float', default='Left', max_length=10, choices=[('Left', 'Left'), ('Right', 'Right')])),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('thumbnail_src', models.CharField(verbose_name='Source', max_length=200, help_text='http://example.com/image.jpg')),
                ('thumbnail_title', models.CharField(verbose_name='Title', max_length=100)),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
        ),
    ]
