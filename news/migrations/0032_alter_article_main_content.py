# Generated by Django 3.2.13 on 2022-10-20 18:07

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0031_auto_20220330_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='main_content',
            field=markdownx.models.MarkdownxField(blank=True, verbose_name='Brødtekst'),
        ),
    ]