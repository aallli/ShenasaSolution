# Generated by Django 3.0.6 on 2020-06-21 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shenasa', '0028_auto_20200621_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalPersonLegalRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('FN', 'Founder'), ('CH', 'Chairman'), ('IN', 'Investor'), ('IF', 'Foreign Investor'), ('IV', 'Venture Capital'), ('IA', 'Angel Investor'), ('ST', 'Stackholder'), ('AC', 'Accelerator'), ('OW', 'Owner'), ('CM', 'Chief Marketing Officer'), ('CC', 'Chief Communication Officer'), ('CE', 'Chief Executive Officer'), ('CT', 'Chief Technical Officer'), ('CF', 'Co Founder')], default='ST', max_length=10, verbose_name='Role')),
                ('number_of_stocks', models.IntegerField(default=0, verbose_name='Number of Stocks')),
                ('amount_of_investment', models.IntegerField(default=0, verbose_name='Amount of Investment (M rls)')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legal_person_legal_role_person', to='Shenasa.LegalPerson', verbose_name='Legal Person')),
                ('target_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legal_person_legal_role_target_person', to='Shenasa.LegalPerson', verbose_name='Legal Person')),
            ],
            options={
                'verbose_name': 'Person Role',
                'verbose_name_plural': 'Person Roles',
                'ordering': ['person', 'role', 'target_person'],
                'abstract': False,
                'unique_together': {('person', 'target_person', 'role')},
            },
        ),
        migrations.CreateModel(
            name='BrandLegalRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('FN', 'Founder'), ('CH', 'Chairman'), ('IN', 'Investor'), ('IF', 'Foreign Investor'), ('IV', 'Venture Capital'), ('IA', 'Angel Investor'), ('ST', 'Stackholder'), ('AC', 'Accelerator'), ('OW', 'Owner'), ('CM', 'Chief Marketing Officer'), ('CC', 'Chief Communication Officer'), ('CE', 'Chief Executive Officer'), ('CT', 'Chief Technical Officer'), ('CF', 'Co Founder')], default='ST', max_length=10, verbose_name='Role')),
                ('number_of_stocks', models.IntegerField(default=0, verbose_name='Number of Stocks')),
                ('amount_of_investment', models.IntegerField(default=0, verbose_name='Amount of Investment (M rls)')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_legal_role_person', to='Shenasa.LegalPerson', verbose_name='Legal Person')),
                ('target_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_legal_role_target_person', to='Shenasa.Brand', verbose_name='Brand')),
            ],
            options={
                'verbose_name': 'Person Role',
                'verbose_name_plural': 'Person Roles',
                'ordering': ['person', 'role', 'target_person'],
                'abstract': False,
                'unique_together': {('person', 'target_person', 'role')},
            },
        ),
    ]
