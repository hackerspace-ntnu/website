# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-09 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20171121_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='userprofile/static/img/default.png', upload_to='profilepictures'),
        ),
    ]
