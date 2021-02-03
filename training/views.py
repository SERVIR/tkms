from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from training.models import Keyword, Resource, Newsreference, Participantorganization, Participant, Trainer, Training
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Count
from django.core import serializers

from .forms import get_newsreference

# Create your views here.
def index(request):
	template_name = "training/index.html"
	return render(request, template_name)
	# return HttpResponse("<h1>SERVIR Trainings</h1><hr><hr>Welcome to the SERVIR training application")

def register(request):
	template_name = "training/register.html"
	return render(request, template_name)

def upcoming(request):
	template_name = "training/upcoming.html"
	return render(request, template_name)
	# return HttpResponse("<h1>Upcoming trainings</h1><hr>Welcome to the SERVIR training application")

def addtraining(request):
	return HttpResponse("<h1>Add a training event</h1><hr>Welcome to the SERVIR training application")

def get_newsreference(request):
	# POST method: process the form data
	if request.method == 'POST':
		form = newsreferenceform(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL
			return HttpResponseRedirect('/newsreferencecaptured/')
		# if GET (or any other method), create a blank form
		else:
			form = newsreferenceform()
		return render(request, 'get_newsreference.html', {'form': form})

@login_required
def events(request):
	order_by = request.GET.get('order_by', 'starts')
	asc_des = request.GET.get('asc_des', 'false')

	if asc_des == '':
		asc_des = 'false'

	event_records = Training.objects.order_by(order_by if asc_des == 'true' else "-" + order_by)
	asc_des = 'true' if asc_des == 'false' else 'false'

	content = {
		'event_records': event_records,
		'info': '',
		'order_by': order_by,
		'asc_des': asc_des,
	}

	return render(request, "training/events.html", context=content)

@login_required
def event_detail(request, eventid):
	# event_data = Training
	event_data = Training.objects.get(id=eventid)
	# TO DO: filter resource_records based on internaluse flag
	resource_data = event_data.resources.all()
	serviceareas_data = event_data.serviceareas.all()
	services_data = event_data.services.all()
	participantorganizations_data = event_data.participantorganizations.all()
	content = {'event_data': event_data,
			   'resource_data': resource_data,
			   'serviceareas_data': serviceareas_data,
			   'services_data': services_data,
			   'participantorganizations_data': participantorganizations_data,
			   'info': '',}
	return render(request, "training/event_detail.html", context=content)

@login_required
def resources(request):
	order_by = request.GET.get('order_by', 'name')
	asc_des = request.GET.get('asc_des', 'true')

	if asc_des == '':
		asc_des = 'false'

	resource_records = Resource.objects.order_by(order_by if asc_des == 'true' else "-" + order_by)
	asc_des = 'true' if asc_des == 'false' else 'false'

	for r in resource_records:
		if Training.objects.filter(resource=r.id).count() > 0:
			r.t = Training.objects.filter(resource=r.id)[0]

	content = {
		'resource_records': resource_records,
		'info': '',
		'order_by': order_by,
		'asc_des': asc_des,
	}

	return render(request, "training/resources.html", context=content)

@login_required
def organizations(request):
	order_by = request.GET.get('order_by', 'country')
	asc_des = request.GET.get('asc_des', 'false')

	if asc_des == '':
		asc_des = 'false'

	organization_records = Participantorganization.objects.order_by(order_by if asc_des == 'true' else "-" + order_by)
	asc_des = 'true' if asc_des == 'false' else 'false'

	content = {
		'organization_records': organization_records,
		'info': '',
		'order_by': order_by,
		'asc_des': asc_des,
	}

	return render(request, "training/organizations.html", context=content)

@login_required
def trainers(request):
	order_by = request.GET.get('order_by', 'name')
	asc_des = request.GET.get('asc_des', 'true')

	if asc_des == '':
		asc_des = 'false'

	trainer_records = Trainer.objects.order_by(order_by if asc_des == 'true' else "-" + order_by)
	asc_des = 'true' if asc_des == 'false' else 'false'

	content = {
		'trainer_records': trainer_records,
		'info': '',
		'order_by': order_by,
		'asc_des': asc_des,
	}
	return render(request, "training/trainers.html", context=content)

def about(request):
	return render(request, "training/about.html",context={})

def charts(request):
	return render(request, "training/charts.html",context={})

### API for TrainingSerializer

from rest_framework import viewsets
from .serializers import TrainingSerializer
import json

class TrainingViewSet(viewsets.ModelViewSet):

	queryset = Training.objects.all().order_by('country')
	serializer_class = TrainingSerializer

	@action(methods=['get'], detail=True)
	def get_training_per_country(self, request, pk=None):
		qs = Training.objects.values('country').annotate(total=Count('country')).order_by('total')
		qs_json = json.dumps(list(qs))
		return HttpResponse(qs_json, content_type='application/json')

class PartecipantViewSet(viewsets.ModelViewSet):

	queryset = Participant.objects.all()

	@action(methods=['get'], detail=True)
	def get_participant_gender_per_country(self, request, pk=None):
		qs = Participant.objects.values('country', 'gender').annotate(total=Count('country')).order_by('total')
		qs_json = json.dumps(list(qs))
		return HttpResponse(qs_json, content_type='application/json')
