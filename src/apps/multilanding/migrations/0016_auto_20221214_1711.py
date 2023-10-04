# Generated by Django 3.2.16 on 2022-12-14 17:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multilanding', '0015_auto_20221208_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='multilanding',
            name='default_lang',
            field=models.CharField(default='tr', max_length=20),
        ),
        migrations.AddField(
            model_name='multilanding',
            name='langs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=['en', 'ru', 'tr', 'de'], size=None),
        ),
    ]