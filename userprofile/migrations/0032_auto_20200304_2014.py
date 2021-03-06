# Generated by Django 3.0.2 on 2020-03-04 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_image_compressed'),
        ('userprofile', '0031_profile_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='thumb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.Image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, to='userprofile.Skill', verbose_name='Ferdigheter'),
        ),
    ]
