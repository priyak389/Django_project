# Generated by Django 5.1.1 on 2024-10-07 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='available',
        ),
    ]
