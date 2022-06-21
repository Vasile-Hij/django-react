from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import City, Note


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            '_id', 
            'username', 
            'email', 
            'name', 
            'isAdmin'
        ]
        
    def get__id(self, obj):
        return obj.id
        
    def get_isAdmin(self, obj):
        return obj.is_staff
        
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
            
        return name
      
        
class  UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            '_id', 
            'username', 
            'email', 
            'name', 
            'isAdmin', 
            'token'
        ]
        
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class CityWeatherSerializer(serializers.Serializer):
    # Location details
    id = serializers.IntegerField()
    city = serializers.StringRelatedField() #read-only
    coutry_code = serializers.StringRelatedField()
    country = serializers.StringRelatedField()
    latitude = serializers.DecimalField(max_digits=6, decimal_places=4, default=0)
    longitude = serializers.DecimalField(max_digits=6, decimal_places=4, default=0)
    # Temperature details
    temperature = serializers.StringRelatedField()
    temperature_max = serializers.StringRelatedField()
    temperature_min = serializers.StringRelatedField()
    temparature_unit = serializers.StringRelatedField()
    # Other weather details
    humidity = serializers.StringRelatedField()
    pressure = serializers.StringRelatedField()
    wind_speed = serializers.StringRelatedField()
    description = serializers.StringRelatedField()

    icon = serializers.StringRelatedField()


class CitySerializer(serializers.ModelSerializer):    
    class Meta:
        model = City
        fields = "__all__"


