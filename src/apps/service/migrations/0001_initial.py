# Generated by Django 3.2.16 on 2022-11-08 14:39

import apps.service.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('image', models.CharField(blank=True, max_length=300, null=True, verbose_name='Category Photo')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='SalonService',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('duration', models.IntegerField(validators=[apps.service.validators.validate_salon_service], verbose_name='Duration')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=30, verbose_name='Gender')),
                ('is_deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='salon_services', to='service.category')),
            ],
            options={
                'verbose_name': 'Salong services',
                'db_table': 'salon.service',
            },
        ),
    ]
