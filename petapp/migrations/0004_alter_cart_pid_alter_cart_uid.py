# Generated by Django 5.1.1 on 2024-10-11 04:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0003_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='pid',
            field=models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='petapp.pet'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='uid',
            field=models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
