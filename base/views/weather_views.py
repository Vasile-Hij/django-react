#!/bin/usr/env python3
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from psycopg2 import IntegrityError

from base.serializers import CitySerializer, CityWeatherSerializer
from base.models import City
from .weather_api import LocationApiService


class CityListAPIView(ListAPIView):
    """ GET cities """
    permission_classes = (IsAuthenticated, )
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer


class CityWeather(APIView):
    """ GET city details """
    permission_classes = (IsAuthenticated,)
    queryset = City.objects.all()

    def post(self, request):
        service = LocationApiService()
    
        city = request.data["city"]
        country = request.data["country"]
        unit = request.data["unit"]

        if country != '':
            location = city + ',' + country
        else:
            location = city

        weather_data = service.current_location_weather(location, unit)
        weather_data['city'] = city.capitalize()

        results = CityWeatherSerializer(weather_data, many=False).data
        return Response(results)


class CitiesWeather(APIView):
    """ GET city """
    permission_classes = (IsAuthenticated,)
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get(self, request):
        service = LocationApiService()
        weather_data = []

        cities = City.objects.all().order_by("name")
        for city in cities:
            weather = service.current_location_weather(city.name, unit="c")
            weather["city"] = city.name
            weather_data.append(weather)

        results = CityWeatherSerializer(weather_data, many=True).data
        return Response(results)


class CityListCreate(ListCreateAPIView):
    """ GET, POST cities """
    permission_classes = (IsAuthenticated, )
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def create(self, request, *args, **kwargs):
        try:
            return super(ListCreateAPIView, self).create(request, *args, **kwargs)
        except IntegrityError:
            # This is due to case sensitivity in the City model.
            return Response(
                data={
                    'error': 'This city is already saved'
                    },
                status=status.HTTP_400_BAD_REQUEST
            )


class CityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """ GET, PUT, PATCH, DELETE cities """
    permission_classes = (IsAuthenticated, )
    queryset = City.objects.all()
    serializer_class = CitySerializer

