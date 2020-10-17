import csv
from io import StringIO

from django.contrib import admin
from django import forms
from django import http
from django import shortcuts
from django.urls import path

import pandas as pd
import numpy as np

# Register your models here.

from .models import Organization
from .models import Training
from .models import Resource
from .models import Newsreference
from .models import Participantorganization
from .models import Participant
from .models import Trainer
from .models import Keyword
from .models import Servicearea
from .models import Service
from .models import Hub
from .models import DataSource

admin.site.register(Organization)
admin.site.register(Hub)
# admin.site.register(Training)
# admin.site.register(Resource)
# admin.site.register(Newsreference)
# admin.site.register(Participantorganization)
# admin.site.register(Participant)
# admin.site.register(Trainer)
admin.site.register(Keyword)
admin.site.register(Servicearea)

admin.site.site_header = "SERVIR Training Knowledge Management System - Administration"

"""
Pending: Implementation of Fieldsets for complex models
example:

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

"""
@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'dataType', 'accessType')
    list_filter = ('accessType','dataType',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'serviceCatalogID', 'servicearea')
    list_filter = ('servicearea',)

@admin.register(Participantorganization)
class ParticipantorganizationAdmin(admin.ModelAdmin):
    """Administration object for Participantorganization models.
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('name', 'acronym', 'organizationtype', 'country')
    list_filter = ('country', 'organizationtype')
    #filter_horizontal = ("trainings",)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    """Administration object for Participant model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('role', 'organization', 'gender','country')
    list_filter = ('country', 'organization')
    #filter_horizontal = ("trainings",)

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    """Administration object for Trainer model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('name','organization','role','gender')
    list_filter = ('role', 'organization')

# class ResourcesInline(admin.TabularInline):
#     """Defines format for insertion of resources"""
#     model=Resource

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    """Administration object for Training model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    object_id = None
    list_display = ('starts', 'name', 'country', 'hub')
    list_filter = ('serviceareas', 'hub', 'recordstatus', 'country')
    filter_horizontal = ('serviceareas', 'services', 'keywords', 'resources', 'dataSource', 'participantorganizations', 'participants', 'trainingorganization', 'trainers')
    fieldsets = (
        (None, {'fields':('name', 'starts', 'ends', 'country', 'city', 'language', 'hub', 'contact', 'recordstatus')}),
        ("Related Services", {
            'classes': ('collapse',),
            'fields':('serviceareas', 'otherservicearea', 'services', 'otherservice')}),
        ("Content", {
            'classes': ('collapse',),
            'fields':('description','expectedoutcome','format','attendance','level','keywords','resources', 'dataSource')}),
        ("Evaluation", {
            'classes': ('collapse',),
            'fields':('presurvey','presurveylink','postsurvey','postsurveylink','newsreferences')}),
        ("Attendance", {
            'classes': ('collapse',),
            'fields':('participantorganizations','participants','trainingorganization', 'trainers','attendanceSheet')}),
        ("Attendance count (if attendance sheet is not available)", {
            'classes': ('collapse',),
            'fields':('attendanceFemales', 'attendanceMales', 'attendanceNotSpecified')}),
        ("Administration", {
            'classes': ('collapse',),
            'fields':('internalnotes','sharedorgnotes')}),
    )
    # inlines = [ResourcesInline]
    
    def import_csv(self, request):
        """ Imports participants from a csv

        Opens a popup, where the user can upload a csv, with this csv
        creates the participants and adds all to the current Training,
        then closes the opened popup. 

        Params:
            request: HttpRequest for this view

        Returns:
            The http response for closing the popup
        """
        # TODO: somehow refresh the widget and show changes
        if request.method == 'POST':
            reader = pd.read_csv(request.FILES['csv_file'],sep=',')
            training = Training.objects.get(id=self.object_id)

            columns = ["Organization","Role","Gender","Country","Presurveycompleted","Postsurveycompleted","Usparticipantstate"]
            print(columns)
            data = pd.DataFrame(np.array(reader), columns=columns)
            print(data)

            for index,df  in reader.iterrows():  
			
                if (df['Presurveycompleted'] == "TRUE"):
                	presurveycompleted = True
                else:
                	presurveycompleted = False

                if (df['Postsurveycompleted'] == "TRUE"):
                	postsurveycompleted = True
                else:
                	postsurveycompleted = False
					
                print(Participantorganization.objects.filter(
                        name=df['Organization'])[0])
				
                participant = Participant.objects.create(
                    organization=Participantorganization.objects.filter(
                        name=df['Organization'])[0],
                    role=df['Role'],
                    gender=df['Gender'],
                    country=df['Country'],
                    presurveycompleted=presurveycompleted,
                    postsurveycompleted=postsurveycompleted,
                    usparticipantstate=df['Usparticipantstate']
                )
                participantorganization = Participantorganization.objects.create(
                    name=df['Organization'],
					organizationtype = "11",
					acronym = df['Organization'][0:10],
					url = "",
					country = df['Country']					
                )
                training.participants.add(participant)
                training.participantorganizations.add(participantorganization)
            training.save()
            return http.HttpResponse(
                '<script type="text/javascript">window.close()</script>')
        form = CsvImportForm()
        payload = {"form": form}
        return shortcuts.render( request, "admin/csv_form.html", payload)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv)),
        ]
        return my_urls + urls

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            self.object_id = obj.id
        form.base_fields['participants'].widget.template_name = (
            "admin/widgets/related_widget_wrapper_batch.html")
        return form


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Administration object for Resource model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('name', 'author', 'added', 'resourcetype', 'hub', 'internaluse')
    list_filter = ('hub', 'internaluse', 'resourcetype', 'author', 'added')
    filter_horizontal = ("trainings",)

@admin.register(Newsreference)
class NewsreferenceAdmin(admin.ModelAdmin):
    """Administration object for Newsreference model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('datepublished', 'title', 'source', 'url')
    list_filter = ('source', 'datepublished')
    filter_horizontal = ("trainings",)
