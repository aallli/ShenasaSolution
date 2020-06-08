# Generated by Django 3.0.6 on 2020-06-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shenasa', '0015_auto_20200608_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='legalrole',
            name='amount_of_investment',
            field=models.IntegerField(default=0, max_length=10, verbose_name='Amount of Investment (M rls)'),
        ),
        migrations.AddField(
            model_name='legalrole',
            name='number_of_shares',
            field=models.IntegerField(default=0, max_length=10, verbose_name='Number of Shares'),
        ),
    ]