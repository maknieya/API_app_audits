# Generated by Django 3.2 on 2021-04-25 22:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audits', '0010_alter_audit_tauxrespect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='tauxEfficacite',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]