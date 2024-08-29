# Generated by Django 4.2.15 on 2024-08-29 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_alter_event_imgbackground'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapeventimage',
            name='description',
            field=models.CharField(default='Niños jugando en el monte', help_text='Enter an image description here', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapeventimage',
            name='title',
            field=models.CharField(default='Juegos', help_text='Enter an image title here', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
