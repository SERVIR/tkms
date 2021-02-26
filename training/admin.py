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

# admin.site.register(Organization)
admin.site.register(Hub)
# admin.site.register(Training)
# admin.site.register(Resource)
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
    list_display = ('starts', 'name', 'country', 'hub', 'get_attendanceMale', 'get_attendanceFemale', 'get_attendanceNotSpecified')
    list_filter = ('serviceareas', 'hub', 'recordstatus', 'country')
    filter_horizontal = ('serviceareas', 'services', 'keywords', 'resources', 'dataSource', 'participantorganizations', 'participants', 'trainingorganization', 'trainers')

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
            'classes': ('collapse',),
            'fields':('serviceareas', 'otherservicearea', 'services', 'otherservice')}),
        ("Content", {
            'classes': ('collapse',),
            'fields':('description','expectedoutcome','attendance','level','keywords','resources', 'dataSource')}),
        ("Evaluation", {
            'classes': ('collapse',),
            'fields':('presurveylink','postsurveylink')}),
        ("Attendance", {
            'classes': ('collapse',),
            'fields':('participantorganizations','participants','trainingorganization', 'trainers')}),
        ("Attendance count (Fill in if attendance sheet is not available)", {
            'classes': ('collapse',),
            'fields':('attendanceFemales', 'attendanceMales', 'attendanceNotSpecified')}),
        ("Administration", {
            'classes': ('collapse',),
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
                participantorganization, created = Participantorganization.objects.get_or_create(
                    name=df['Organization'],
                    organizationtype = "11",
                    acronym = df['Organization'][0:10],
                    url = "",
                    country = df['Country']
                )
                training.participants.add(participant)
                training.participantorganizations.add(participantorganization)

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
