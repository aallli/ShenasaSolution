# Generated by Django 3.0.6 on 2020-06-21 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shenasa', '0030_auto_20200621_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandlegalrole',
            name='role',
            field=models.CharField(choices=[('FN', 'Founder'), ('CH', 'Chairman'), ('VC', 'Vice Chairman'), ('MB', 'Member of the Board'), ('IN', 'Investor'), ('IF', 'Foreign Investor'), ('IV', 'Venture Capital'), ('IA', 'Angel Investor'), ('ST', 'Stockholder'), ('AC', 'Accelerator'), ('OW', 'Owner'), ('CM', 'Chief Marketing Officer'), ('CC', 'Chief Communication Officer'), ('CE', 'Chief Executive Officer'), ('CT', 'Chief Technical Officer'), ('CF', 'Co Founder')], default='ST', max_length=10, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='brandpersonrole',
            name='role',
            field=models.CharField(choices=[('FN', 'Founder'), ('CH', 'Chairman'), ('VC', 'Vice Chairman'), ('MB', 'Member of the Board'), ('IN', 'Investor'), ('IF', 'Foreign Investor'), ('IV', 'Venture Capital'), ('IA', 'Angel Investor'), ('ST', 'Stockholder'), ('AC', 'Accelerator'), ('OW', 'Owner'), ('CM', 'Chief Marketing Officer'), ('CC', 'Chief Communication Officer'), ('CE', 'Chief Executive Officer'), ('CT', 'Chief Technical Officer'), ('CF', 'Co Founder')], default='ST', max_length=10, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='legalpersonlegalrole',
            name='role',
            field=models.CharField(choices=[('FN', 'Founder'), ('CH', 'Chairman'), ('VC', 'Vice Chairman'), ('MB', 'Member of the Board'), ('IN', 'Investor'), ('IF', 'Foreign Investor'), ('IV', 'Venture Capital'), ('IA', 'Angel Investor'), ('ST', 'Stockholder'), ('AC', 'Accelerator'), ('OW', 'Owner'), ('CM', 'Chief Marketing Officer'), ('CC', 'Chief Communication Officer'), ('CE', 'Chief Executive Officer'), ('CT', 'Chief Technical Officer'), ('CF', 'Co Founder')], default='ST', max_length=10, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='legalpersonpersonrole',
            name='role',
            field=models.CharField(choices=[('FN', 'Founder'), ('CH', 'Chairman'), ('VC', 'Vice Chairman'), ('MB', 'Member of the Board'), ('IN', 'Investor'), ('IF', 'Foreign Investor'), ('IV', 'Venture Capital'), ('IA', 'Angel Investor'), ('ST', 'Stockholder'), ('AC', 'Accelerator'), ('OW', 'Owner'), ('CM', 'Chief Marketing Officer'), ('CC', 'Chief Communication Officer'), ('CE', 'Chief Executive Officer'), ('CT', 'Chief Technical Officer'), ('CF', 'Co Founder')], default='ST', max_length=10, verbose_name='Role'),
        ),
    ]