# Generated by Django 3.2.16 on 2022-12-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multilanding', '0008_auto_20221205_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='multilanding',
            name='sub_domain',
            field=models.CharField(db_index=True, default=None, max_length=50, verbose_name='Sub domain'),
            preserve_default=False,
        ),
    ]
