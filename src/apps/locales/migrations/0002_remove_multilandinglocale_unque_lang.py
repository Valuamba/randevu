# Generated by Django 3.2.16 on 2022-11-24 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='multilandinglocale',
            name='unque_lang',
        ),
    ]
