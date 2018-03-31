# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-24 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_tags', to='inventory.Tag'),
        ),
    ]