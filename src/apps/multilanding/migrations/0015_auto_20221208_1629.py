# Generated by Django 3.2.16 on 2022-12-08 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multilanding', '0014_auto_20221208_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='multilanding',
            name='end_work_time_step',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='multilanding',
            name='start_work_time_step',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='multilanding',
            name='sub_domain',
            field=models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Sub domain'),
        ),
    ]
