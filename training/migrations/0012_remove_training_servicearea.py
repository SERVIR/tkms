# Generated by Django 2.1.5 on 2020-03-04 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0011_auto_20200304_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='servicearea',
        ),
    ]