# Generated by Django 3.0.2 on 2021-04-13 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_remove_rule_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='internal',
            field=models.BooleanField(default=False, verbose_name='Intern regel'),
        ),
    ]
