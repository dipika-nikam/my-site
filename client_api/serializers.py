from pyexpat import model
from rest_framework import serializers

from api.models import Service
from .models import AppointmentModel,BeauticianAvailabilities,BeauticianServices


class AppointmentSerlizer(serializers.ModelSerializer):
  appointment_service = []
  class Meta:
    model = AppointmentModel
    exclude = ['user_id',]

class AvailabilitiesSerializers(serializers.ModelSerializer):
  class Meta:
    model = BeauticianAvailabilities
    fields ='__all__'


class BeauticianServicesSerializer(serializers.ModelSerializer):
  class Meta:
    model = BeauticianServices
    fields ='__all__'

class BeauticianServicesSerializerget(serializers.ModelSerializer):
  class Meta:
    model = BeauticianServices
    fields =['services_id',]
