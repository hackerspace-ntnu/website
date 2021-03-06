# Generated by Django 3.0.2 on 2020-10-12 19:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_auto_20190512_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deregistration_end',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Avmeldingsfrist'),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_limit',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Maks påmeldte'),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_end',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Påmeldingsfrist'),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Påmeldingsstart'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_end',
            field=models.DateTimeField(null=True, verbose_name='Sluttidspunkt'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_start',
            field=models.DateTimeField(null=True, verbose_name='Starttidspunkt'),
        ),
    ]
