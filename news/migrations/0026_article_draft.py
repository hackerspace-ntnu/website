# Generated by Django 3.0.2 on 2020-11-16 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0025_merge_20201026_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='draft',
            field=models.BooleanField(default=False, verbose_name='Utkast'),
        ),
    ]