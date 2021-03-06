# Generated by Django 3.1.2 on 2020-10-20 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Navn')),
                ('stock', models.IntegerField(verbose_name='Lagerbeholdning')),
                ('description', models.CharField(max_length=200, verbose_name='Beskrivelse')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='Bilde')),
            ],
        ),
    ]
