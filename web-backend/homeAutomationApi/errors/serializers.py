from rest_framework import serializers
from devices.serializers import prefetch_device_serializer
from .models import error_log

class error_log_serializer(serializers.ModelSerializer):
    device = prefetch_device_serializer()
    class Meta:
        model = error_log
        fields = ['id', 'description', 'device', 'date']