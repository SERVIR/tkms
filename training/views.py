from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from training.models import Keyword, Organization, Resource, Newsreference, Participantorganization, Participant, Trainer, Training

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

def events(request):
	event_records = Training.objects.order_by('starts')
	content = {'event_records': event_records,
			   'info': '',}
	return render(request, "training/events.html", context=content)

def event_detail(request, eventid):
	# event_data = Training
	event_data = Training.objects.get(id=eventid)
	content = {'event_data': event_data,
			   'info': '',}
	return render(request, "training/event_detail.html", context=content)

def resources(request):
	resource_records = Resource.objects.order_by('resourcetype')
	content = { 'resource_records': resource_records,
		'info':'',}
	return render(request, "training/resources.html", context=content)

def organizations(request):
	# Participant Organizations, rather than organizers
	organization_records = Participantorganization.objects.order_by('country')
	content = {'organization_records': organization_records,
			   'info': '',}
	return render(request, "training/organizations.html", context=content)

def trainers(request):
	trainer_records = Trainer.objects.order_by('name')
	content = {'trainer_records': trainer_records,
			   'info': '',}
	return render(request, "training/trainers.html", context=content)

def about(request):
	return render(request, "training/about.html",context={})