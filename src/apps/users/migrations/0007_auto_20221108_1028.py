# Generated by Django 3.2.16 on 2022-11-08 10:28

from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Full Name'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.CharField(blank=True, max_length=300, verbose_name='Photo Ref'),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('working', 'Working'), ('not_working', 'Not working'), ('removed', 'Removed')], default=django.utils.timezone.now, max_length=30, verbose_name='Position'),
            preserve_default=False,
        ),
    ]
