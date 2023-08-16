from dataclasses import fields
from rest_framework import serializers
from .models import alert
from devices.serializers import prefetch_device_serializer
from drf_extra_fields.fields import Base64ImageField
from devices.models import device

class alert_serializer(serializers.ModelSerializer):
    device = prefetch_device_serializer(read_only=True)
    class Meta:
        model = alert
        fields = ['id', 'description', 'device', 'date', 'type', 'image']
 
class create_alert_device_serializer(serializers.ModelSerializer):
    class Meta:
        model = device
        fields = ['unit_id'] 
        
class create_alert_serializer(serializers.ModelSerializer):
    class Meta:
        model = alert
        fields = ['id', 'description', 'device', 'date', 'type', 'image']


        