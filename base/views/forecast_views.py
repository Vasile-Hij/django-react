from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def weatherNow(request):
    return Response (f'to do next')