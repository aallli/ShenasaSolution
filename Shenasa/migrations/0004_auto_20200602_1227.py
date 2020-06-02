# Generated by Django 3.0.6 on 2020-06-02 12:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shenasa', '0003_auto_20200602_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturalperson',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Profile Image'),
        ),
        migrations.AddField(
            model_name='naturalperson',
            name='mobile',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\d{9,15}$')], verbose_name='Mobile'),
        ),
    ]
