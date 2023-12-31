# Generated by Django 3.2.16 on 2022-11-11 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_alter_staffschedule_week_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffbreak',
            name='steps_amount',
        ),
        migrations.AddField(
            model_name='staffbreak',
            name='end_break_time_step',
            field=models.IntegerField(default=40, verbose_name='Steps amount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffschedule',
            name='week_day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Sunday'), (6, 'Saturday')], verbose_name='Week day'),
        ),
    ]
