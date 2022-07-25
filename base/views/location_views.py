#!/bin/usr/env python3
from django.core.checks import messages
from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from psycopg2 import IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from base.models import Location, UsersLocations
from base.serializers import (LocationSerializer, 
                              UsersLocationsSerializer)


unit_validator = {
        "celsius_short" : "c",
        "celsius_long": "celsius",
        "celsius": "metric",
        "imperial_short": "f",
        "imperial_long": "fahrenheit",
        "imperial": "imperial"
    }


"""
    user permissions
    params: addLocation, getMyLocation, getMyLocations, updateLocationUnit, deleteMyLocation
"""

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addLocation(request):
    user = request.user
    data = request.data
             
    city=data['city']
    country_code=data['country_code']
    country=data['country']
    unit=data['unit']  
    
    
    if unit == "":
        pass # consider that user has no preferences
    elif unit not in unit_validator.values():
        message = {"unit can be":'metric: c or celsius | imperial: f or fahrenheit | kelvin: k or kelvin'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    else:
        unit = ""   
    
    
    if country_code == "":
        message = {"message":"provide country code, e.g. for Ireland is 'ie' "}
        return Response(message, status=status.HTTP_201_CREATED)
    elif not country_code.isaplha():
        message = {"message":'Other characters for country code than strings are not accepted!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    elif country_code > 2:
        message = {"message":"Country code accepted is 2 letters only, e.g. for Ireland is 'ie' "}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
     
        
    if country == "":
        pass
    elif not country.isalpha():
        message = {"message":'Other characters for country than strings are not accepted!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        
    try:
        """
            Any user will create the locations only once, and other users will retrieve only 
            that location. If location exists is assigned to the users.
        """

        new_or_existing_city = Location.objects.get_or_create(
            city=city, 
            country_code=country_code,
            country=country)
        existing_city = Location.objects.get(
            city=city, 
            country_code=country_code,
            country=country)
        
        already_exists = existing_city.location_city.filter(user=user).exists()
        if already_exists:
            message = {'detail':'This city already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST) 
        else:
            add_user_city = UsersLocations.objects.create(
                user=user,
                location_city=existing_city,
                unit=unit)
            add_user_city.save()
            
    except NameError:
        message = {"message":"Please provide city name"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UsersLocationsSerializer(add_user_city, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyLocation(request, pk):
    user = request.user

    try:
        my_city = user.my_locations.get(id=pk)
    except UsersLocations.DoesNotExist:
        message = {"message":'Please provide right id'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        message = {"message":'Other characters than integer are not accepted!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    except IndexError:
        message = {"message":'Please insert user_location id!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
      
    serializer = UsersLocationsSerializer(my_city, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyLocations(request):
    user = request.user
    my_cities = user.my_locations.all()
    serializer = UsersLocationsSerializer(my_cities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateLocationUnit(request, pk):
    
    """
       User can update location unit only
       :params: function check firstly if any other field than unit is trying to update,
                user can update only his locations,
                and units allowed are only them in the validator dictionary,
                if correct, new_unit is saved.
    """
    
    user = request.user
    data = request.data
    
    city=data['city']
    country_code=data['country_code']
    country=data['country']
     
    if city or country_code or country != "":
        message = {"message": "You cannot to perform this action. Please search another city!"}
        return Response(message, status=status.HTTP_403_FORBIDDEN)
    
    new_units = UsersLocations.objects.filter(user=user)
    new_unit = new_units.get(id=pk) 
    
    
    if user != new_units:
        message = {"Warning":"You are not the right user to do this!"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)
    
    new_unit.unit=data['unit']
    
    
    if new_unit == "":
        message = message = {"unit can be":'metric: c or celsius | imperial: f or fahrenheit | kelvin: k or kelvin'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)
    elif new_unit not in unit_validator.values():
        message = {"unit can be":'metric: c or celsius | imperial: f or fahrenheit | kelvin: k or kelvin'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)  
        
    new_unit.save()

    serializer = UsersLocationsSerializer(new_unit, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteMyLocation(request, pk):
    user = request.user
    cityToDelete = user.my_locations.get(id=pk)
    cityToDelete.delete()
    return Response(f'City of {cityToDelete} deleted', status=status.HTTP_200_OK)
