# Generated by Django 2.2.1 on 2019-05-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_queue_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
