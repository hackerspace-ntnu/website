# Generated by Django 2.0.10 on 2019-05-12 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0020_auto_20190507_0150'),
        ('news', '0019_auto_20190512_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userprofile.Profile'),
        ),
        migrations.AddField(
            model_name='event',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userprofile.Profile'),
        ),
    ]
