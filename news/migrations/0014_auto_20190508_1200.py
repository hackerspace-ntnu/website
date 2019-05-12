# Generated by Django 2.0.10 on 2019-05-08 12:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_event_servering'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2019, 5, 8, 12, 0, 27, 50736), verbose_name='Sluttdato'),
        ),
        migrations.AddField(
            model_name='event',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2019, 5, 8, 12, 0, 27, 50723), verbose_name='Startdato'),
        ),
        migrations.AddField(
            model_name='event',
            name='hour_end',
            field=models.TimeField(default=datetime.datetime(2019, 5, 8, 12, 0, 27, 50754), verbose_name='Slutttidspunkt'),
        ),
        migrations.AddField(
            model_name='event',
            name='hour_start',
            field=models.TimeField(default=datetime.datetime(2019, 5, 8, 12, 0, 27, 50745), verbose_name='Starttidspunkt'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_end',
            field=models.DateTimeField(null=True, verbose_name='Slutt tidspunkt'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_start',
            field=models.DateTimeField(null=True, verbose_name='Start tidspunkt'),
        ),
    ]