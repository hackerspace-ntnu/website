# Generated by Django 3.1.2 on 2020-10-21 01:35

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_item_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Beskrivelse'),
        ),
    ]