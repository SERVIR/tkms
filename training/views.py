from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.staticfiles.storage import staticfiles_storage
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
	order_by = request.GET.get('order_by', 'starts')

	asc_des = request.GET.get('asc_des', 'false')

	if asc_des == '':
		asc_des = 'false';


	asc_url = "https://img.icons8.com/ultraviolet/2x/generic-sorting-2.png"
	asc_url_starts = ''
	asc_url_name = ''
	asc_url_country = ''
	asc_url_hub = ''
	asc_url_format = ''

	if order_by == 'starts':
		if asc_des == 'true':
			asc_url_starts = "https://img.icons8.com/ultraviolet/2x/generic-sorting-2.png"
		else:
			asc_url_starts = "https://img.icons8.com/ultraviolet/2x/generic-sorting.png"

	if order_by == 'name':
		if asc_des == 'true':
			asc_url_name = "https://img.icons8.com/ultraviolet/2x/generic-sorting-2.png"
		else:
			asc_url_name = "https://img.icons8.com/ultraviolet/2x/generic-sorting.png"

	if order_by == 'country':
		if asc_des == 'true':
			asc_url_country = "https://img.icons8.com/ultraviolet/2x/generic-sorting-2.png"
		else:
			asc_url_country = "https://img.icons8.com/ultraviolet/2x/generic-sorting.png"

	if order_by == 'hub':
		if asc_des == 'true':
			asc_url_hub = "https://img.icons8.com/ultraviolet/2x/generic-sorting-2.png"
		else:
			asc_url_hub = "https://img.icons8.com/ultraviolet/2x/generic-sorting.png"

	if order_by == 'format':
		if asc_des == 'true':
			asc_url_format = "https://img.icons8.com/ultraviolet/2x/generic-sorting-2.png"
		else:
			asc_url_format = "https://img.icons8.com/ultraviolet/2x/generic-sorting.png"




	if asc_des == 'false':
		order_by = "-"+order_by
		event_records = Training.objects.order_by(order_by)
		asc_url = "https://img.icons8.com/ultraviolet/2x/generic-sorting.png";
		asc_des = 'true'
	else:		
		event_records = Training.objects.order_by(order_by)
		asc_des = 'false'
		

	content = {'event_records': event_records,
			   'info': '',
			   'asc_url_starts': asc_url_starts, 
			   'asc_url_name': asc_url_name, 
			   'asc_url_country': asc_url_country, 
			   'asc_url_hub': asc_url_hub, 
			   'asc_url_format': asc_url_format, 
			   'asc_des': asc_des, 
			   }
	return render(request, "training/events.html", context=content)

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

def resources(request):
	order_by = request.GET.get('order_by', 'name')
	asc_des = request.GET.get('asc_des', 'true')

	if asc_des == '':
		asc_des = 'false'

	asc_image = 'training/generic-sorting-2.png' if asc_des == 'true' else 'training/generic-sorting.png'
	asc_url = staticfiles_storage.url(asc_image)
	asc_url_name = asc_url if order_by == 'name' else ''
	asc_url_author = asc_url if order_by == 'author' else ''
	asc_url_resourcetype = asc_url if order_by == 'resourcetype' else ''

	if asc_des == 'false':
		order_by = "-" + order_by
		resource_records = Resource.objects.order_by(order_by)
		asc_des = 'true'
	else:
		resource_records = Resource.objects.order_by(order_by)
		asc_des = 'false'

	for r in resource_records:
		if Training.objects.filter(resource=r.id).count() > 0:
			r.t = Training.objects.filter(resource=r.id)[0]
		
	content = {
		'resource_records': resource_records,
		'info': '',
		'asc_url_name': asc_url_name,
		'asc_url_author': asc_url_author,
		'asc_url_resourcetype': asc_url_resourcetype,
		'asc_des': asc_des,
	}

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

def charts(request):
	return render(request, "training/charts.html",context={})

### API for TrainingSerializer

from rest_framework import viewsets
from .serializers import TrainingSerializer

class TrainingViewSet(viewsets.ModelViewSet):
	#queryset = Training.objects.all().order_by('hub')
	queryset = Training.objects.all().order_by('country')
	#attendanceFemales
	serializer_class = TrainingSerializer