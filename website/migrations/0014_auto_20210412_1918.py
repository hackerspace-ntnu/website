# Generated by Django 3.1.1 on 2021-04-12 19:18

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_rule_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
