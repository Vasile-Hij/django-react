#!/bin/usr/env python3
from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from psycopg2 import IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.serializers import CitySerializer, ForecastSerializer
from base.models import City, UsersLocations
from .weather_api import LocationApiService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addCity(request):
    user = request.user
    data = request.data
         
    locationService = LocationApiService()
    
    city=data['city']
    country_code=data['country_code']
    country=data['country']
    unit=data['unit']     
         
    new_city = City.objects.create(
        location=city,
        country=country,
        country_code=country_code
    )
    new_city.save()
    new_city.userTag.set([user])
                    
    if country != '':
        location = ','.join([city, country])
    else:
        location = city

    weather_data = locationService.current_location_weather(location, unit)
    weather_data['city'] = city.capitalize()
       
    serializer = CitySerializer(weather_data, many=False)
    return Response(serializer.data)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyCity(request, pk):
    user = request.user
    city = user.cities.get(id=pk)
    serializer = CitySerializer(city, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyCities(request):
    user = request.user
    my_cities = City.objects.filter(userTag__id=user.id)
    serializer = CitySerializer(my_cities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getCities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateCity(request, pk):
    user = request.user
    city = user.user_search_cities.get(id=pk)
    serializer = CitySerializer(city, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCity(request, pk):
    city = City.objects.get(id=pk)
    city.delete()
    return Response('City deleted')

