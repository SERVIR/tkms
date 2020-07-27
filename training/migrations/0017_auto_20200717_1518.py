# Generated by Django 3.0.8 on 2020-07-17 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0016_resource_hub'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='hub',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='training.Hub'),
        ),
        migrations.AddField(
            model_name='training',
            name='trainingorganization',
            field=models.ManyToManyField(help_text='Participating Organizations (Trainers)', related_name='training_orgs', to='training.Participantorganization'),
        ),
        migrations.AlterField(
            model_name='training',
            name='participantorganizations',
            field=models.ManyToManyField(help_text='Participating Organizations (Trainees)', to='training.Participantorganization'),
        ),
    ]