# Generated by Django 2.0.13 on 2019-03-26 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_auto_20190325_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='comment',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]