# Generated by Django 2.1.5 on 2020-03-04 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0010_auto_20200304_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='otherservice',
            field=models.CharField(blank=True, help_text='Other Service (non-officialy recognized)', max_length=100),
        ),
        migrations.AddField(
            model_name='training',
            name='services',
            field=models.ManyToManyField(to='training.Service'),
        ),
        migrations.AlterField(
            model_name='training',
            name='contact',
            field=models.CharField(blank=True, help_text='Contact email(s)', max_length=200),
        ),
    ]
