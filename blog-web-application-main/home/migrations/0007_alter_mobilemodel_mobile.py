# Generated by Django 4.1.7 on 2023-04-16 07:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_rename_mbolemodel_mobilemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilemodel',
            name='mobile',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]