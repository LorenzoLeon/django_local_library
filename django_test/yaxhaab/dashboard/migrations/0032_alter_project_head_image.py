# Generated by Django 4.2.15 on 2024-09-23 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_remove_mapeventimage_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='head_image',
            field=models.ImageField(help_text='', null=True, upload_to='images/'),
        ),
    ]
