# Generated by Django 3.0.8 on 2020-07-17 16:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_auto_20200605_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hub_region', models.IntegerField(choices=[(0, 'Global'), (1, 'Eastern & Southern Africa'), (2, 'Hindu Kush Himalaya'), (3, 'Lower Mekong River'), (4, 'West Africa'), (5, 'Amazonia'), (6, 'Central America')])),
                ('hub_short_name', models.IntegerField(blank=True, choices=[(0, 'SERVIR SCO'), (1, 'SERVIR E&SA'), (2, 'SERVIR HKH'), (3, 'SERVIR Mekong'), (4, 'SERVIR WA'), (5, 'SERVIR Amazonia'), (6, 'SERVIR Centralamerica')], help_text='Short Name')),
                ('hub_logo', models.ImageField(blank=True, help_text='SERVIR Region Logo', upload_to='')),
                ('org_name', models.CharField(default='', help_text='Hub Organization or Consortium Lead', max_length=200)),
                ('org_acronym', models.CharField(max_length=50)),
                ('org_url', models.URLField(blank=True, default='http://', help_text='Organization Site')),
                ('org_logo', models.ImageField(blank=True, help_text='Organization Logo', upload_to='')),
                ('org_address', models.CharField(max_length=500)),
                ('org_phone', models.CharField(max_length=20)),
                ('primary_contact_email', models.EmailField(blank=True, help_text='Primary Contact Email', max_length=254)),
                ('primary_contact_name', models.CharField(blank=True, help_text='Primary Contact Name', max_length=200)),
                ('primary_contact_role', models.CharField(blank=True, help_text='Primary Contact Role', max_length=200)),
                ('cblead_name', models.CharField(blank=True, help_text='Capacity Building Lead', max_length=200)),
                ('cblead_email', models.EmailField(blank=True, help_text='Capacity Building email', max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='hub',
            field=models.CharField(default='', help_text='Hub Name', max_length=100),
        ),
        migrations.AddField(
            model_name='resource',
            name='added',
            field=models.DateField(default=datetime.datetime.now, help_text='Date the resource was added', verbose_name='Date Added'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(default='', help_text='Hub Organization/Consortium Lead', max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='url',
            field=models.URLField(blank=True, default='http://', help_text='Organization Site'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='location',
            field=models.URLField(blank=True, default='https://', help_text='URL for the resource'),
        ),
    ]