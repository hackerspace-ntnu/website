# Generated by Django 3.1.1 on 2021-04-12 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='description',
            field=models.CharField(default='Regel', max_length=500, verbose_name='Beskrivelse'),
            preserve_default=False,
        ),
    ]
