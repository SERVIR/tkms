from django.contrib import admin

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

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    """Administration object for Participant model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('role', 'organization', 'gender','country')
    list_filter = ('country', 'organization')

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

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    """Administration object for Training model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
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

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Administration object for Resource model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('name', 'author', 'added', 'resourcetype', 'hub', 'internaluse')
    list_filter = ('hub', 'internaluse', 'resourcetype', 'author', 'added')

@admin.register(Newsreference)
class NewsreferenceAdmin(admin.ModelAdmin):
    """Administration object for Newsreference model
    Defines:
    - fields to be displayed in list view (list_display)
    - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('datepublished', 'title', 'source', 'url')
    list_filter = ('source', 'datepublished')
