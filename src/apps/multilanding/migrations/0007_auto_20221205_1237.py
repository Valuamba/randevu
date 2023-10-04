# Generated by Django 3.2.16 on 2022-12-05 12:37

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multilanding', '0006_rename_cover_img_multilanding_cover'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MultilandingGallery',
        ),
        migrations.RemoveField(
            model_name='multilanding',
            name='user',
        ),
        migrations.AddField(
            model_name='multilanding',
            name='gallery',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200, null=True), default=None, size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='multilanding',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='multilanding', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='multilanding',
            name='domain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_domains', to='multilanding.multilandingdomain'),
        ),
    ]
