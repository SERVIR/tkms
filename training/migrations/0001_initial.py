# Generated by Django 2.2.7 on 2019-12-04 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('keyword',),
            },
        ),
        migrations.CreateModel(
            name='Newsreference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Article title', max_length=255)),
                ('datepublished', models.DateField(help_text='Date Published', null=True)),
                ('url', models.URLField(help_text='Location of the article')),
                ('source', models.CharField(help_text='Publisher', max_length=100, null=True)),
                ('abstract', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('source',),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('acronym', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=500)),
                ('url', models.URLField()),
                ('logo', models.ImageField(upload_to='')),
                ('email', models.EmailField(max_length=254)),
                ('cb_lead', models.CharField(max_length=200)),
                ('region', models.IntegerField(blank=True, choices=[(1, 'Eastern & Southern Africa'), (2, 'Hindu Kush Himalaya'), (3, 'Lower Mekong River'), (4, 'West Africa'), (5, 'Amazonia'), (6, 'Central America')])),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(help_text='Role within organization', max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('country', models.CharField(help_text='Country of residence', max_length=100)),
                ('presurveycompleted', models.BooleanField()),
                ('postsurveycompleted', models.BooleanField()),
                ('usparticipantstate', models.CharField(blank=True, help_text='State (for US participants only)', max_length=3)),
            ],
            options={
                'ordering': ('country', 'organization', 'role'),
            },
        ),
        migrations.CreateModel(
            name='Participantorganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('organizationtype', models.IntegerField(choices=[(1, 'Academic Institution'), (2, 'Consortium'), (3, 'Federal/Central Government'), (4, 'Intergovernmental Organization'), (5, 'Local Government'), (6, 'Private Sector (For-Profit)'), (7, 'Private Sector (Non-Profit)/Voluntary/NGO'), (8, 'Research Institution'), (9, 'State/Provincial Government'), (10, 'Tribal Entity'), (11, 'Miscellaneous/Other')], default=1, help_text='Organization Type')),
                ('acronym', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(help_text='Primary location (HQ)', max_length=100)),
            ],
            options={
                'ordering': ('country', 'acronym'),
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('resourcetype', models.IntegerField(choices=[(1, 'Training Agenda'), (2, 'Training Notes'), (3, 'Document'), (4, 'Presentation'), (5, 'Exercise guide'), (6, 'Tutorial'), (7, 'Video'), (8, 'Audio'), (9, 'Script'), (10, 'Dataset'), (11, 'External website'), (12, 'Photo/Photo gallery'), (13, 'Other')], default=1, help_text='Resource Type')),
                ('location', models.URLField()),
                ('internaluse', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=100)),
                ('abstract', models.TextField(blank=True, help_text='Brief description of the resource')),
                ('backedup', models.BooleanField(blank=True, default=False, help_text='Indicates whether the resource has been backed up')),
                ('backuplocation', models.URLField(blank=True, help_text='Indicates the backup location')),
                ('keywords', models.ManyToManyField(to='training.Keyword')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('role', models.CharField(help_text='Role within organization', max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.Participantorganization')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('servicearea', models.IntegerField(choices=[(1, 'Agriculture & Food Security'), (2, 'Land Cover Land Use Change & Ecosystems'), (3, 'Water & Water Related Disasters'), (4, 'Weather & Climate')], default=1, help_text='Service Area')),
                ('starts', models.DateField()),
                ('ends', models.DateField(blank=True)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, help_text='Brief description of the training')),
                ('expectedoutcome', models.TextField(blank=True, help_text='Expected Outcome')),
                ('format', models.IntegerField(choices=[(1, 'In-person training'), (2, 'Online training'), (3, 'Workshop'), (4, 'Hackathon'), (5, 'Exchange')], default=1)),
                ('language', models.CharField(blank=True, max_length=100)),
                ('attendance', models.IntegerField(choices=[(1, 'By Invitation'), (2, 'Open Registration')], default=1)),
                ('level', models.IntegerField(choices=[(1, 'Basic'), (2, 'Intermediate'), (3, 'Advanced')], default=1, help_text='Experience Level')),
                ('contact', models.EmailField(blank=True, help_text='Contact email', max_length=254)),
                ('presurvey', models.BooleanField(blank=True, help_text='Is there a pre-training survey?')),
                ('presurveylink', models.URLField(blank=True, help_text='Location of pre-survey link')),
                ('postsurvey', models.BooleanField(blank=True, help_text='Is there a post-training survey?')),
                ('postsurveylink', models.URLField(blank=True, help_text='Location of post-survey link')),
                ('internalnotes', models.TextField(blank=True, help_text='Notes for internal users (SERVIR network)')),
                ('sharedorgnotes', models.URLField(blank=True, help_text='Shared documents (e.g., Google Drive Document/Folder, Sharepoint site, etc.)')),
                ('keywords', models.ManyToManyField(blank=True, to='training.Keyword')),
                ('newsreferences', models.ManyToManyField(blank=True, to='training.Newsreference')),
                ('organization', models.ForeignKey(help_text='Host Organization', on_delete=django.db.models.deletion.CASCADE, to='training.Organization')),
                ('participantorganizations', models.ManyToManyField(to='training.Participantorganization')),
                ('participants', models.ManyToManyField(blank=True, to='training.Participant')),
                ('resources', models.ManyToManyField(blank=True, to='training.Resource')),
                ('trainers', models.ManyToManyField(blank=True, to='training.Trainer')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.Participantorganization'),
        ),
    ]
