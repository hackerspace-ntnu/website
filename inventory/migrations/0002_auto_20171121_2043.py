# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-21 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='column',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='row',
            field=models.IntegerField(null=True),
        ),
    ]