# Generated by Django 3.1.1 on 2021-03-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0036_auto_20210312_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='ends',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='starts',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
