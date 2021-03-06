# Generated by Django 3.1.1 on 2021-03-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0031_auto_20210301_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantorganization',
            name='organizationtype',
            field=models.IntegerField(choices=[(0, '-- NOT SPECIFIED --'), (1, 'Academic Institution'), (2, 'Consortium'), (3, 'Federal/Central Government'), (4, 'Intergovernmental Organization'), (5, 'Local Government'), (6, 'Private Sector (For-Profit)'), (7, 'Private Sector (Non-Profit)/Voluntary/NGO'), (8, 'Research Institution'), (9, 'State/Provincial Government'), (10, 'Indigenous Peoples Organization'), (11, 'Miscellaneous/Other')], default=0, help_text='Organization Type'),
        ),
    ]
