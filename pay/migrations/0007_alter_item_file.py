# Generated by Django 5.0.2 on 2024-02-28 08:59

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0006_alter_item_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='file',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='pay/static/img/'), upload_to='.'),
        ),
    ]
