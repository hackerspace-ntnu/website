# Generated by Django 3.0.2 on 2020-03-11 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0037_auto_20200311_1217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
