# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-17 18:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rpi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raspberrypi',
            old_name='lastSeen',
            new_name='last_seen',
        ),
        migrations.AlterField(
            model_name='raspberrypi',
            name='mac',
            field=models.CharField(db_index=True, default='12:34:56:78:90:ab', max_length=17, unique=True,
                                   validators=[django.core.validators.RegexValidator('^([a-f0-9]{2}:){5}[a-f0-9]{2}$')],
                                   verbose_name='MAC'),
        ),
        migrations.AlterField(
            model_name='raspberrypi',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
