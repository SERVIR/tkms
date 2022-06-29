import csv
from io import StringIO

from django.contrib import admin
from django import forms
from django import http
from django import shortcuts
from django.urls import path

import pandas as pd
import numpy as np

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.

# from .models import Organization
from .models import Training
from .models import Resource
from .models import Participantorganization
from .models import Participant
from .models import Trainer
from .models import Keyword
from .models import Servicearea
from .models import Service
from .models import Hub
from .models import DataSource

admin.site.site_header = "SERVIR Training Knowledge Management System - Administration"

class ServiceareaResource(resources.ModelResource):
    class Meta:
        model = Servicearea

@admin.register(Servicearea)
class ServiceareaAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = ServiceareaResource

class KeywordResource(resources.ModelResource):
    class Meta:
        model = Keyword

@admin.register(Keyword)
class KeywordAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = KeywordResource

class HubResource(resources.ModelResource):
    class Meta:
        model = Hub

@admin.register(Hub)
class KeywordAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = HubResource

class DataSourceResource(resources.ModelResource):
    class Meta:
        model = DataSource

@admin.register(DataSource)
class DataSourceAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('id', 'name', 'dataType', 'accessType')
    list_filter = ('accessType','dataType',)
    search_fields = ('name', 'id')
    resource_class = DataSourceResource

class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service

@admin.register(Service)
class ServiceAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('id', 'name', 'serviceCatalogID', 'servicearea')
    list_filter = ('servicearea',)
    search_fields = ('name', 'id')
    resource_class = ServiceResource

class ParticipantorganizationResource(resources.ModelResource):
    class Meta:
        model = Participantorganization

# ------------------------------------------
# Participant Organization Form
# ------------------------------------------
@admin.register(Participantorganization)
class ParticipantorganizationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    """Administration object for Participantorganization models.
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('id', 'name', 'acronym', 'organizationtype', 'country')
    list_filter = ('organizationtype', 'country')
    filter_horizontal = ("trainee_participation","trainer_participation",)
    search_fields = ('name', 'acronym', 'country', 'id')
    ordering = ['country','acronym','name']
    resource_class = ParticipantorganizationResource

class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant

@admin.register(Participant)
class ParticipantAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    """Administration object for Participant model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('id', 'role', 'organization', 'gender','country')
    list_filter = ('country', 'organization')
    #filter_horizontal = ("trainings",)
    search_fields = ('role', 'organization__name', 'country', 'id')
    autocomplete_fields = ['organization']
    resource_class = ParticipantResource


# ------------------------------------------
# TRAINER Form
# ------------------------------------------

class TrainingInline (admin.TabularInline):
    model = Training.trainers.through

class TrainerResource(resources.ModelResource):
    class Meta:
        model = Trainer

@admin.register(Trainer)
class TrainerAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    """Administration object for Trainer model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('id', 'name', 'role', 'gender', 'organization',)
    list_filter = ('gender', 'organization__country')
    search_fields = ('name', 'organization__name', 'organization__country', 'role', 'id')
    filter_horizontal = ('trainings',)
    # exclude = ('trainings',)
    # inlines = [TrainingInline]
    resource_class = TrainerResource

# class ResourcesInline(admin.TabularInline):
#     """Defines format for insertion of resources"""
#     model=Resource

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class TrainingResource(resources.ModelResource):
    class Meta:
        model = Training

@admin.register(Training)
class TrainingAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    """Administration object for Training model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    object_id = None
    list_display = ('id', 'starts', 'name', 'country', 'hub', 'get_attendanceMale', 'get_attendanceFemale', 'get_attendanceNotSpecified')
    list_filter = ('serviceareas', 'hub', 'recordstatus', 'country', 'language')
    filter_horizontal = ('serviceareas', 'services', 'keywords', 'resources', 'dataSource', 'participantorganizations', 'participants', 'trainingorganization', 'trainers')
    date_hierarchy = "starts"
    search_fields = ("name", "country", "serviceareas__name", "expectedoutcome", "description", "trainingorganization__name", "id")

    def get_attendanceFemale(self, obj):
        return obj.attendanceFemales
    get_attendanceFemale.short_description = "F"

    def get_attendanceMale(self, obj):
        return obj.attendanceMales
    get_attendanceMale.short_description = "M"

    def get_attendanceNotSpecified(self, obj):
        return obj.attendanceNotSpecified
    get_attendanceNotSpecified.short_description = "N/S"

    fieldsets = (
        (None, {'fields':('name', 'starts', 'ends', 'format', 'country', 'city', 'language', 'hub', 'contact', 'recordstatus')}),
        ("Related Services", {
            'classes': ('collapse-open',),
            'fields':('serviceareas', 'otherservicearea', 'services', 'otherservice')}),
        ("Content", {
            'classes': ('collapse-open',),
            'fields':('description','expectedoutcome','attendance','level','keywords','resources', 'dataSource')}),
        ("Evaluation", {
            'classes': ('collapse-open',),
            'fields':('presurveylink','postsurveylink')}),
        ("Attendance", {
            'classes': ('collapse-open',),
            'fields':('participantorganizations','participants','trainingorganization', 'trainers')}),
        ("Attendance count (Fill in if attendance sheet is not available)", {
            'classes': ('collapse-open',),
            'fields':('attendanceFemales', 'attendanceMales', 'attendanceNotSpecified')}),
        ("Administration", {
            'classes': ('collapse-open',),
            'fields':('internalnotes','sharedorgnotes')}),
    )
    # inlines = [ResourcesInline]

    change_form_template = "admin/forms/training-admin-form.html"

    def response_change(self, request, obj):
        return super().response_change(request, obj)

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
            training.participants.clear()
            # training.participants.remove(*training.participants.all())

            columns = ["Organization","Role","Gender","Country","Presurveycompleted","Postsurveycompleted","Usparticipantstate"]
            data = pd.DataFrame(np.array(reader), columns=columns)

            attendance = {"F": 0, "M": 0, "X": 0}

            for index,df  in reader.iterrows():

                gender = "X" if df['Gender'] not in ("F", "M", "X") else df['Gender']
                if gender == "F": attendance["F"] += 1
                elif gender == "M": attendance["M"] += 1
                else: attendance["X"] += 1

                presurveycompleted = True if df['Presurveycompleted'] == "TRUE" else False
                postsurveycompleted = True if df['Postsurveycompleted'] == "TRUE" else False

                participantorganization, created = Participantorganization.objects.get_or_create(
                    name=df['Organization'],
                    country = df['Country']
                )
                training.participantorganizations.add(participantorganization)
                participant, created = Participant.objects.get_or_create(
                    organization=Participantorganization.objects.filter(
                        name=df['Organization'])[0],
                        role=df['Role'],
                        gender=gender,
                        country=df['Country'],
                        presurveycompleted=presurveycompleted,
                        postsurveycompleted=postsurveycompleted,
                        usparticipantstate=df['Usparticipantstate']
                )
                training.participants.add(participant)

            training.attendanceFemales = attendance.get("F", 0)
            training.attendanceMales = attendance.get("M", 0)
            training.attendanceNotSpecified = attendance.get("X", 0)

            training.save()
            return http.HttpResponse(
                '<script type="text/javascript">window.opener.location.reload();window.close();</script>')
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
        return form

    resource_class = TrainingResource

class ResourceResource(resources.ModelResource):
    class Meta:
        model = Resource


@admin.register(Resource)
class ResourceAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    """Administration object for Resource model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('id', 'name', 'author', 'added', 'resourcetype', 'hub', 'internaluse', 'backedup')
    list_filter = ('hub', 'internaluse', 'backedup', 'resourcetype', 'license', 'author', 'added')
    filter_horizontal = ("trainings",)
    search_fields = ("name", "author",)
    date_hierarchy = "added"
    fieldsets = (
        (None, {'fields':('name', 'resourcetype', 'location', 'added', 'hub', 'internaluse', 'author', 'abstract', 'keywords', 'license', 'trainings')}),
        ("Backup Status", {
            'classes': ('collapse-open'),
            'fields':('backedup', 'backuplocation', )})
    )
    resource_class = ResourceResource
