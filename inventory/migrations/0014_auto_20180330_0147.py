# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-30 01:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20180329_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='loanitem',
            name='loan',
        ),
        migrations.DeleteModel(
            name='LoanItem',
        ),
    ]