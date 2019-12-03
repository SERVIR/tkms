import datetime

from django.db import models
from django.utils import timezone


# Create your models here.

class Keyword(models.Model):
	keyword = models.CharField(max_length=100)
	class Meta:
		ordering = ('keyword',)
	def __str__(self):
		return self.keyword

class Organization(models.Model):
	REGION_CHOICES = (
		(1, "Eastern & Southern Africa"),
		(2, "Hindu Kush Himalaya"),
		(3, "Lower Mekong River"),
		(4, "West Africa"),
		(5, "Amazonia"),
		(6, "Central America")
	)
	name = models.CharField(max_length=200)
	acronym = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	address = models.CharField(max_length=500)
	url = models.URLField()
	logo = models.ImageField()
	email = models.EmailField()
	cb_lead = models.CharField(max_length=200)
	region = models.IntegerField(choices=REGION_CHOICES, blank=True)
	def __str__(self):
		return self.acronym

	def region_verbose(self):
		return dict(Organization.REGION_CHOICES)[self.region]

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
		(9, "Script"),
		(10, "Dataset"),
		(11, "External website"),
		(12, "Photo/Photo gallery"),
		(13, "Other")
	)
	name = models.CharField(max_length=300)
	resourcetype = models.IntegerField(choices=RESOURCE_TYPE_CHOICES, default=1, help_text="Resource Type")
	location = models.URLField()
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
	country = models.CharField(max_length=100, help_text="Primary location (HQ)")
	class Meta:
		ordering = ('country', 'acronym',)
	def __str__(self):
		return self.country + ", " + self.acronym

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
	SERVICE_AREA_CHOICES = (
		(1, "Agriculture & Food Security"),
		(2, "Land Cover Land Use Change & Ecosystems"),
		(3, "Water & Water Related Disasters"),
		(4, "Weather & Climate")
		)
	LEVEL_CHOICES = (
		(1, "Basic"),
		(2, "Intermediate"),
		(3, "Advanced")
	)
	name = models.CharField(max_length=300)
	servicearea = models.IntegerField(choices=SERVICE_AREA_CHOICES, default=1, help_text="Service Area")
	starts = models.DateField()
	ends = models.DateField(blank=True)
	# application_deadline = models.DateField(blank=True)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	description = models.TextField(blank=True, help_text="Brief description of the training")
	# audience = models.CharField(max_length=2500, blank=True)
	expectedoutcome = models.TextField(blank=True, help_text="Expected Outcome")
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, help_text="Host Organization")
	format = models.IntegerField(choices=FORMAT_CHOICES, default=1)
	language = models.CharField(max_length=100, blank=True)
	attendance = models.IntegerField(choices=ATTENDANCE_CHOICES, default=1)
	# qualifications = models.CharField(max_length=2500, blank=True)
	level = models.IntegerField(choices=LEVEL_CHOICES, default=1, help_text="Experience Level")
	contact = models.EmailField(blank=True, help_text="Contact email")
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
	participantorganizations = models.ManyToManyField(Participantorganization)
	participants = models.ManyToManyField(Participant, blank=True)
	trainers = models.ManyToManyField(Trainer, blank=True)
	internalnotes = models.TextField(blank=True, help_text="Notes for internal users (SERVIR network)")

	def __str__(self):
		return self.name + ", " + self.country

	def servicearea_verbose(self):
		return dict(Training.SERVICE_AREA_CHOICES)[self.servicearea]

	def format_verbose(self):
		return dict(Training.FORMAT_CHOICES)[self.format]

	def level_verbose(self):
		return dict(Training.LEVEL_CHOICES)[self.level]

	def attendance_verbose(self):
		return dict(Training.ATTENDANCE_CHOICES)[self.attendance]

