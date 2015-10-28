# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Textbox',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('header_text', models.CharField(verbose_name='Header', max_length=100)),
                ('header_fontsize', models.IntegerField(verbose_name='Fontsize', default=32)),
                ('header_color', models.CharField(verbose_name='Color', default='#505050', help_text='RGB-code', max_length=7)),
                ('header_fontfamily', models.CharField(verbose_name='Font family', default='sans-serif', max_length=100)),
                ('text_text', models.TextField(verbose_name='Text', max_length=10000)),
                ('text_columns', models.IntegerField(verbose_name='Columns', default=1)),
                ('text_fontsize', models.IntegerField(verbose_name='Fontsize', default=18)),
                ('text_color', models.CharField(verbose_name='Color', default='#505050', help_text='RGB-code', max_length=7)),
                ('text_fontfamily', models.CharField(verbose_name='Font family', default='sans-serif', max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='Publication date')),
            ],
            options={
                'verbose_name_plural': 'textboxes',
            },
        ),
    ]
