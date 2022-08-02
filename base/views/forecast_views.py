from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response, Serializer
from psycopg2 import IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from base.models import (Location, 
                         UsersLocations, 
                         ForecastHourly, 
                         ForecastNow)
from base.serializers import (LocationSerializer, 
                              UsersLocationsSerializer, 
                              ForecastHourlySerializer, 
                              ForecastNowSerializer)

from .location_service.weather_api import LocationApiService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weatherNow(request, pk):
    user = request.user
    data = request.data
    
    location_api_service = LocationApiService()
    
   
    
    my_city = user.my_locations.get(id=pk)
    if user.is_staff or my_city.user == user:
       
        user_location_serializer = UsersLocationsSerializer(my_city, many=False)
        custom_serializer = user_location_serializer.data
    
        city = custom_serializer['location_city']['city']
        country_code = custom_serializer['location_city']['country_code']
        unit = custom_serializer['unit']
        
        if country_code != "":
            location = city + "," + country_code
        else:
            location = city
        
        
        forecast_now = location_api_service.current_location_weather(location, unit)
        forecast_now["city"] = city
        
        serializer = ForecastNowSerializer(forecast_now, many=False)
        return Response(serializer.data)

   
