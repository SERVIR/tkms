# Generated by Django 2.2.7 on 2019-12-04 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0003_training_sharedorgnotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantorganization',
            name='url',
            field=models.URLField(blank=True, help_text='Organization Site'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='url',
            field=models.URLField(blank=True, help_text='Organization Site'),
        ),
    ]
