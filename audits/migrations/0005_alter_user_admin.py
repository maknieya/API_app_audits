# Generated by Django 3.2 on 2021-04-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audits', '0004_alter_user_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
