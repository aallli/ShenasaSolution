# Generated by Django 3.0.6 on 2020-06-08 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shenasa', '0013_auto_20200608_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='personrole',
            name='amount_of_investment',
            field=models.IntegerField(default=0, verbose_name='Amount of Investment'),
        ),
        migrations.AddField(
            model_name='personrole',
            name='number_of_shares',
            field=models.IntegerField(default=0, verbose_name='Number of Shares'),
        ),
    ]
