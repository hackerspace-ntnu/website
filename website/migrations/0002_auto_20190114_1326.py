# Generated by Django 2.0.10 on 2019-01-14 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='thumbnail_dark_text',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='card',
            name='body',
            field=models.TextField(max_length=200),
        ),
    ]
