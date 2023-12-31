# Generated by Django 3.2.16 on 2022-12-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_appointment_status'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='appointment',
            name='unique_employee',
        ),
        migrations.RemoveIndex(
            model_name='appointment',
            name='appointment_employe_cb56b8_idx',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='date',
            new_name='day',
        ),
        migrations.AddIndex(
            model_name='appointment',
            index=models.Index(fields=['employee', 'day'], name='appointment_employe_ac2327_idx'),
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(fields=('employee', 'day', 'time_step'), name='unique_employee'),
        ),
    ]
