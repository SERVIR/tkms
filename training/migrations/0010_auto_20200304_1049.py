# Generated by Django 2.1.5 on 2020-03-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0009_auto_20200304_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='otherservicearea',
            field=models.CharField(blank=True, help_text='Other Service Area (non-officialy recognized)', max_length=100),
        ),
        migrations.AddField(
            model_name='training',
            name='serviceareas',
            field=models.ManyToManyField(to='training.Servicearea'),
        ),
    ]