from rest_framework import serializers

from .models import Training, Servicearea, Service, Organization

class TrainingSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Training
       depth = 1
       # To do: Include 'serviceareas', 'services'
       fields = ('name', 'starts', 'ends', 'country', 'description', 'trainingorganization')
