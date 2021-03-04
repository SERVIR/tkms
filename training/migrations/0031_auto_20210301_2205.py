# Generated by Django 3.1.1 on 2021-03-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0030_auto_20210226_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='role',
            field=models.CharField(blank=True, help_text='Role within organization', max_length=200),
        ),
        migrations.AlterField(
            model_name='training',
            name='participantorganizations',
            field=models.ManyToManyField(blank=True, help_text='Participating Organizations (Trainees)', to='training.Participantorganization'),
        ),
    ]