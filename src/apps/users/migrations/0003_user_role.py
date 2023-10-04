# Generated by Django 4.0.6 on 2022-10-23 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin'), ('employee', 'Employee')], default=20, max_length=20, verbose_name='User role'),
            preserve_default=False,
        ),
    ]