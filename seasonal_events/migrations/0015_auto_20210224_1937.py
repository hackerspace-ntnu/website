# Generated by Django 3.1.2 on 2021-02-24 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seasonal_events', '0014_season_disable_reservations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='banner_color',
        ),
        migrations.RemoveField(
            model_name='season',
            name='banner_text',
        ),
    ]
