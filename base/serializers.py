from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import (Note, Location, 
                         UsersLocations, 
                         ForecastHourly, 
                         ForecastNow)


class NoteSerializer(ModelSerializer):
    icon = serializers.StringRelatedField()
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
    
    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id', 
            'city', 
            'country', 
            'country_code',
            'user'
            ]
                        
                
class UsersLocationsSerializer(serializers.ModelSerializer):
    location_city = serializers.SerializerMethodField(read_only=True)
    #user = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UsersLocations
        fields = [
                'id',
                'location_city',
                #'user',
                'unit'
                ]
 
    def get_location_city(self, obj):
        user_location_city = obj.location_city
        serializer = LocationSerializer(user_location_city, many=False)
        return serializer.data
        
    #def get_user(self, obj):
    #    user = obj.user
    #    serializer = UserSerializer(user, many=False)
    #    return serializer.data
        
        
class ForecastHourlySerializer(serializers.ModelSerializer):
    icon = serializers.CharField(read_only=True)
    
    class Meta:
        model = ForecastHourly
        fields = [
            'id', 
            'city', 
            'created_at', 
            'updated_at', 
            'temperature', 
            'feels_like',
            'temperature_unit',
            'humidity',
            'pressure',
            'wind_speed', 
            'description', 
            'icon'
            ]
        
        
class ForecastNowSerializer(serializers.ModelSerializer):
    icon = serializers.CharField(read_only=True)
    
    class Meta:
        model = ForecastNow
        fields = [
            'city',
            'country_code', 
            'country', 
            'temperature', 
            'temperature_max',
            'temperature_min',
            'temperature_unit',
            'humidity',
            'pressure',
            'wind_speed', 
            'description', 
            'icon'
        ]