# Generated by Django 4.2.15 on 2024-08-29 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_remove_mapevent_map'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='imgbackground',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
