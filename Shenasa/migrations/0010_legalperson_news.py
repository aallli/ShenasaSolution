# Generated by Django 3.0.6 on 2020-06-05 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shenasa', '0009_auto_20200605_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='legalperson',
            name='news',
            field=models.ManyToManyField(related_name='legal_person_news', to='Shenasa.News', verbose_name='News'),
        ),
    ]