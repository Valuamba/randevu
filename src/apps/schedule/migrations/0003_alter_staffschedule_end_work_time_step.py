# Generated by Django 3.2.16 on 2022-11-10 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20221110_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffschedule',
            name='end_work_time_step',
            field=models.IntegerField(null=True, verbose_name='End work time step'),
        ),
    ]
