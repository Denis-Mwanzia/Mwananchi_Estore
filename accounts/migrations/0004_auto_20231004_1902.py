# Generated by Django 3.1 on 2023-10-04 16:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20231001_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
        ),
    ]
