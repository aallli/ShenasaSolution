# Generated by Django 3.0.6 on 2020-06-02 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shenasa', '0002_auto_20200602_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legalperson',
            name='CEO',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shenasa.NaturalPerson', verbose_name='CEO'),
        ),
    ]
