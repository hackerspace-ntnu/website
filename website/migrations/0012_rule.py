# Generated by Django 3.1.1 on 2021-04-12 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20210322_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Tittel')),
                ('body', models.TextField()),
                ('priority', models.IntegerField(default=0)),
            ],
        ),
    ]
