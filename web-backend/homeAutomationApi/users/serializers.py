from rest_framework import serializers
from .models import allowed_person, custom_profile

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = custom_profile
        fields = '__all__'
        write_only = ['password']
        
    def create(self, validated_data):
        user = custom_profile(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class allowed_person_serializer(serializers.ModelSerializer):
    class Meta:
        model = allowed_person
        fields = '__all__'