# Generated by Django 4.2.15 on 2024-08-28 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointsinstance',
            name='size',
            field=models.IntegerField(default=1, help_text='Size for this Map Point'),
        ),
    ]
