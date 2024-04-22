from rest_framework import serializers
from .models import DeliveryLocation, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class DeliveryLocationSerializer(serializers.ModelSerializer): 
    
    user = UserSerializer()

    class Meta:
        model = DeliveryLocation
        fields = ['id', 'user', 'address', 'point']

class AgeGroupSerializer(serializers.Serializer):
    age_group = serializers.CharField()
    count = serializers.IntegerField()