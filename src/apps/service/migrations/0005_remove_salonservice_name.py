# Generated by Django 3.2.16 on 2022-11-25 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20221124_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salonservice',
            name='name',
        ),
    ]
