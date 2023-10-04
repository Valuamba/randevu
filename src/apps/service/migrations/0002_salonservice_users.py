# Generated by Django 3.2.16 on 2022-11-09 15:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salonservice',
            name='users',
            field=models.ManyToManyField(null=True, related_name='services', to=settings.AUTH_USER_MODEL),
        ),
    ]
