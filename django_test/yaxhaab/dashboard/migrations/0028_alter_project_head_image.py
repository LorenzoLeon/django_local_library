# Generated by Django 4.2.15 on 2024-09-09 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_alter_project_head_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='head_image',
            field=models.ImageField(help_text='', null=True, upload_to='images/'),
        ),
    ]
