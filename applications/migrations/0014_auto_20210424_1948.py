# Generated by Django 3.1.6 on 2021-04-24 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0013_auto_20210424_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='group_choice',
            field=models.ManyToManyField(through='applications.ApplicationGroupChoice', to='applications.ApplicationGroup'),
        ),
        migrations.AlterField(
            model_name='applicationgroupchoice',
            name='priority',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
