import datetime
from datetime import datetime

from django.db import models
from django.utils import timezone


# Create your models here.

class Keyword(models.Model):
	keyword = models.CharField(max_length=100)
	class Meta:
		ordering = ('keyword',)
	def __str__(self):
		return self.keyword

class DataSource(models.Model):
	DATA_TYPE_CHOICES = (
		(0, "Other/not specified"),
		(1, "EO Sensor"),
		(2, "Model")
	)
	ACCESS_TYPE_CHOICES = (
		(0, "Other/not specified"),
		(1, "Public/Open Source"),
		(2, "Commercial"),
		(3, "Restricted by Originator")
	)
	name = models.CharField(max_length=100)
	dataType = models.IntegerField(choices=DATA_TYPE_CHOICES, blank=True)
	accessType = models.IntegerField(choices=ACCESS_TYPE_CHOICES, blank=True)

	class Meta:
		ordering = ('name',)
	def __str__(self):
		return self.name

class Organization(models.Model):
	REGION_CHOICES = (
		(1, "Eastern & Southern Africa"),
		(2, "Hindu Kush Himalaya"),
		(3, "Lower Mekong River"),
		(4, "West Africa"),
		(5, "Amazonia"),
		(6, "Central America")
	)
	hub = models.CharField(max_length=100, help_text="Hub Name", default="")
	name = models.CharField(max_length=200, help_text="Hub Organization/Consortium Lead", default="")
	acronym = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	address = models.CharField(max_length=500)
	url = models.URLField(help_text="Organization Site", default="http://", blank=True)
	logo = models.ImageField()
	email = models.EmailField()
	cb_lead = models.CharField(max_length=200)
	region = models.IntegerField(choices=REGION_CHOICES, blank=True)
	def __str__(self):
		return self.acronym

	def region_verbose(self):
		return dict(Organization.REGION_CHOICES)[self.region]

# 2020-07-17: Hub model will replace Organization model in a second step, after the records
# 			  from Organization have been copied and references have been updated in related models

class Hub(models.Model):

	hub_short_name = models.CharField(max_length=100, help_text='Hub Short Name')
	hub_region = models.CharField(max_length=100, help_text='Region Name')
	hub_logo = models.ImageField(help_text="SERVIR Region Logo", blank=True)

	org_name = models.CharField(max_length=200, help_text="Hub Organization or Consortium Lead", default="")
	org_acronym = models.CharField(max_length=50)
	org_url = models.URLField(help_text="Organization Site", default="http://", blank=True)
	org_logo = models.ImageField(help_text="Organization Logo", blank=True)
	org_address = models.CharField(max_length=500, help_text="Postal Address", blank=True)
	org_phone = models.CharField(max_length=20, help_text="Phone Number", blank=True)

	# Primary Organization Contact Info
	primary_contact_email = models.EmailField(help_text="Primary Contact Email", blank=True)
	primary_contact_name = models.CharField(max_length=200, help_text="Primary Contact Name", blank=True)
	primary_contact_role = models.CharField(max_length=200, help_text="Primary Contact Role", blank=True)

	# Capacity Building Lead Contact Info
	cblead_name = models.CharField(max_length=200, help_text="Capacity Building Lead", blank=True)
	cblead_email = models.EmailField(help_text="Capacity Building email", blank=True)

	def __str__(self):
		return self.hub_short_name


class Resource(models.Model):
	RESOURCE_TYPE_CHOICES = (
		(1, "Training Agenda"),
		(2, "Training Notes"),
		(3, "Document"),
		(4, "Presentation"),
		(5, "Exercise guide"),
		(6, "Tutorial"),
		(7, "Video"),
		(8, "Audio"),
		(9, "Script/Code Repository"),
		(10, "Dataset"),
		(11, "External website"),
		(12, "Photo/Photo gallery"),
		(13, "Document Repository"),
		(14, "Debrief"),
		(0, "Other")
	)
	name = models.CharField(max_length=300)
	resourcetype = models.IntegerField(choices=RESOURCE_TYPE_CHOICES, default=1, help_text="Resource Type")
	location = models.URLField(blank=True, help_text="URL for the resource", default="https://")
	added = models.DateField(default=datetime.now, help_text="Date the resource was added", verbose_name="Date Added")
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE, default=1)
	internaluse = models.BooleanField(blank=True, default=False)
	author = models.CharField(max_length=100, blank=True)
	abstract = models.TextField(blank=True, help_text="Brief description of the resource")
	keywords = models.ManyToManyField(Keyword)
	backedup = models.BooleanField(blank=True, default=False, help_text="Indicates whether the resource has been backed up")
	backuplocation = models.URLField(blank=True, help_text="Indicates the backup location")
	def __str__(self):
		return self.name
	def resourcetype_verbose(self):
		return dict(Resource.RESOURCE_TYPE_CHOICES)[self.resourcetype]


class Newsreference(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255, help_text="Article title")
	datepublished = models.DateField(help_text="Date Published", null=True)
	url = models.URLField(help_text="Location of the article")
	source = models.CharField(max_length=100, help_text="Publisher", null=True)
	abstract = models.TextField(blank=True)
	class Meta:
		ordering = ('source',)
	def __str__(self):
		return self.title

class Participantorganization(models.Model):
	ORGANIZATION_TYPE_CHOICES = (
		(1, "Academic Institution"),
		(2, "Consortium"),
		(3, "Federal/Central Government"),
		(4, "Intergovernmental Organization"),
		(5, "Local Government"),
		(6, "Private Sector (For-Profit)"),
		(7, "Private Sector (Non-Profit)/Voluntary/NGO"),
		(8, "Research Institution"),
		(9, "State/Provincial Government"),
		(10, "Tribal Entity"),
		(11, "Miscellaneous/Other")
	)
	name = models.CharField(max_length=200)
	organizationtype = models.IntegerField(choices=ORGANIZATION_TYPE_CHOICES, default=1, help_text="Organization Type")
	acronym = models.CharField(max_length=50, blank=True)
	url = models.URLField(blank=True, help_text="Organization Site")
	country = models.CharField(max_length=100, help_text="Primary location (HQ)")
	class Meta:
		ordering = ('country', 'acronym',)
	def __str__(self):
		return self.country + ", " + self.acronym + " " + self.name

	def organizationtype_verbose(self):
		return dict(Participantorganization.ORGANIZATION_TYPE_CHOICES)[self.organizationtype]


class Participant(models.Model):
	GENDER_CHOICES = (
		("M", "Male"),
		("F", "Female")
	)
	organization = models.ForeignKey(Participantorganization, on_delete=models.CASCADE)
	role = models.CharField(max_length=200, help_text="Role within organization")
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
	country = models.CharField(max_length=100, help_text="Country of residence")
	presurveycompleted = models.BooleanField()
	postsurveycompleted = models.BooleanField()
	usparticipantstate = models.CharField(max_length=3, help_text="State (for US participants only)", blank=True)
	class Meta:
		ordering = ('country', 'organization', 'role')
	def __str__(self):
		return self.country + ", " + self.role

	def gender_verbose(self):
		return dict(Participant.GENDER_CHOICES)[self.gender]

class Servicearea(models.Model):
	name = models.CharField(max_length=300, help_text="Service Area Name")

	def __str__(self):
		return self.name

class Service(models.Model):
	name = models.CharField(max_length=300, help_text="Service Name (According to the Service Catalog)")
	serviceCatalogID = models.CharField(max_length=40, blank=True, help_text="Service Catalog ID")
	servicearea = models.ForeignKey(Servicearea, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Trainer(models.Model):
	GENDER_CHOICES = (
		("M", "Male"),
		("F", "Female")
	)
	name = models.CharField(max_length=300)
	organization = models.ForeignKey(Participantorganization, on_delete=models.CASCADE)
	role = models.CharField(max_length=200, help_text="Role within organization")
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")

	def __str__(self):
		return self.name

	def gender_verbose(self):
		return dict(Trainer.GENDER_CHOICES)[self.gender]

class Training(models.Model):
	FORMAT_CHOICES = (
		(1, "In-person training"),
		(2, "Online training"),
		(3, "Workshop"),
		(4, "Hackathon"),
		(5, "Exchange")
		)
	ATTENDANCE_CHOICES = (
		(1, "By Invitation"),
		(2, "Open Registration")
		)
	LEVEL_CHOICES = (
		(1, "Basic"),
		(2, "Intermediate"),
		(3, "Advanced")
	)
	LEAD_CHOICES = (
		(1, "Hub"),
		(2, "SCO"),
		(3, "AST"),
		(4, "SME"),
		(5, "Support Team"),
		(6, "Partner"),
		(7, "Contractor"),
		(8, "Other")
	)
	STATUS_CHOICES = (
		(0, "Draft/test"),
		(1, "Work in Progress"),
		(2, "Registration Complete"),
	)
	name = models.CharField(max_length=300)
	# servicearea = models.IntegerField(choices=SERVICE_AREA_CHOICES, default=1, help_text="Service Area")
	serviceareas = models.ManyToManyField(Servicearea, blank=True)
	otherservicearea = models.CharField(max_length=100, blank=True, help_text="Other Service Area (non-officialy recognized)")
	services = models.ManyToManyField(Service, blank=True)
	otherservice = models.CharField(max_length=100, blank=True, help_text="Other Service (non-officialy recognized)")
	starts = models.DateField(blank=True)
	ends = models.DateField(blank=True)
	# application_deadline = models.DateField(blank=True)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	description = models.TextField(blank=True, help_text="Brief description of the training")
	# audience = models.CharField(max_length=2500, blank=True)
	expectedoutcome = models.TextField(blank=True, help_text="Expected Outcome")
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, help_text="Host Organization")
	hub = models.ForeignKey(Hub, on_delete=models.CASCADE, default=1)
	lead = models.IntegerField(choices=LEAD_CHOICES, default=1, help_text="Type of organization leading the event")
	format = models.IntegerField(choices=FORMAT_CHOICES, default=1)
	language = models.CharField(max_length=100, blank=True)
	attendance = models.IntegerField(choices=ATTENDANCE_CHOICES, default=1)
	# qualifications = models.CharField(max_length=2500, blank=True)
	level = models.IntegerField(choices=LEVEL_CHOICES, default=1, help_text="Experience Level")
	contact = models.CharField(max_length=200, blank=True, help_text="Contact email(s)")
	# fees = models.BooleanField()
	# promoimage = models.URLField(blank=True, name="Promo Image")
	# promovideo = models.URLField(blank=True, name= "Promo Video")
	presurvey = models.BooleanField(help_text="Is there a pre-training survey?", blank=True)
	presurveylink = models.URLField(help_text="Location of pre-survey link", blank=True)
	postsurvey = models.BooleanField(help_text="Is there a post-training survey?", blank=True)
	postsurveylink = models.URLField(help_text="Location of post-survey link", blank=True)
	keywords = models.ManyToManyField(Keyword, blank=True)
	resources = models.ManyToManyField(Resource, blank=True)
	newsreferences = models.ManyToManyField(Newsreference, blank=True)
	participantorganizations = models.ManyToManyField(Participantorganization, help_text="Participating Organizations (Trainees)")
	trainingorganization = models.ManyToManyField(Participantorganization, help_text="Participating Organizations (Trainers)", related_name="training_orgs")
	participants = models.ManyToManyField(Participant, blank=True)
	trainers = models.ManyToManyField(Trainer, blank=True)
	# trainingorganization = models.ManyToManyRel()
	internalnotes = models.TextField(blank=True, help_text="Notes for internal users (SERVIR network)")
	sharedorgnotes = models.URLField(blank=True, help_text="Shared documents (e.g., Google Drive Document/Folder, Sharepoint site, etc.)")
	recordstatus = models.IntegerField(choices=STATUS_CHOICES, default=0)
	dataSource = models.ManyToManyField(DataSource, help_text="Data sources used in the training", blank=True)

	def __str__(self):
		return self.name + ", " + self.country

	# def servicearea_verbose(self):
	# 	return dict(Training.SERVICE_AREA_CHOICES)[self.servicearea]

	def format_verbose(self):
		return dict(Training.FORMAT_CHOICES)[self.format]

	def level_verbose(self):
		return dict(Training.LEVEL_CHOICES)[self.level]

	def attendance_verbose(self):
		return dict(Training.ATTENDANCE_CHOICES)[self.attendance]

	def lead_verbose(self):
		return dict(Training.LEAD_CHOICES)[self.lead]
