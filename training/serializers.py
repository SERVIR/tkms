from rest_framework import serializers

from .models import Training, Servicearea, Service

class ParticipantsSerializer(serializers.RelatedField):
     def to_representation(self, value):
         return value.role

     class Meta:
        model = Training

class TrainingSerializer(serializers.HyperlinkedModelSerializer):
   participants = ParticipantsSerializer(read_only=True, many=True)
   class Meta:
       model = Training
       depth = 1
       # To do: Include 'serviceareas', 'services'
       #fields = ('name', 'starts', 'ends', 'country', 'description', 'trainingorganization')
       fields = ('country', 'attendanceFemales', 'attendanceMales', 'participants')
