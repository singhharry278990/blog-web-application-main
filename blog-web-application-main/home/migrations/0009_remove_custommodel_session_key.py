# Generated by Django 4.2 on 2023-04-17 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_custommodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custommodel',
            name='session_key',
        ),
    ]
