# Generated by Django 3.0.2 on 2020-02-11 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0027_auto_20200211_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termsofservice',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]