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

admin.site.register(Organization)
admin.site.register(Training)
admin.site.register(Resource)
admin.site.register(Newsreference)
admin.site.register(Participantorganization)
admin.site.register(Participant)
admin.site.register(Trainer)
admin.site.register(Keyword)

admin.site.site_header = "SERVIR Training Knowledge Management System - Administration"

