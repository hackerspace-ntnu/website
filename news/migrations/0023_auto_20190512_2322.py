# Generated by Django 2.0.10 on 2019-05-12 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0022_auto_20190512_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='file',
            field=models.FileField(blank=True, upload_to='event-uploads'),
        ),
    ]
