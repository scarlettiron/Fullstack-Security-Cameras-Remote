from dataclasses import field
from rest_framework import serializers
from .models import device, device_passcode, local_server


class local_server_serialzer(serializers.ModelSerializer):
    class Meta:
        model = local_server
        fields = '__all__'
        read_only_fields = ['pk', 'unit_id']
        
                
class device_passcodes_serializer(serializers.ModelSerializer):
    class Meta:
        model = device_passcode
        fields = ['code', 'id', 'device']



class prefetch_device_serializer(serializers.ModelSerializer):
    class Meta:
        model  = device
        fields = '__all__'
        

class device_serializer(serializers.ModelSerializer):
    lock_codes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = device
        fields = ['id', 'name', 'type', 'ip_address', 'url', 'model', 'pair', 
                  'unit_id', 'household', 'lock_codes']
        read_only_fields = ['id', 'unit_id']
    
    def get_lock_codes(self, obj):
        if obj.type.lower() != 'lock':
            return 
        
        try:
            passcodes = device_passcode.objects.filter(device = obj)
            serializer = device_passcodes_serializer(passcodes, many=True)
            return serializer.data
        except:
            return None
    

        
    