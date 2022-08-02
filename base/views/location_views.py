#!/bin/usr/env python3
from django.core.checks import messages
from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from psycopg2 import IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import Location, UsersLocations
from base.serializers import (LocationSerializer, 
                              UsersLocationsSerializer)

valid_units = { 
    "unit0":"",           
    "unit1": "celsius",
    "unit2": "fahrenheit",
    "unit3": "imperial",
    "unit4": "kelvin",
    "unit5": "c",
    "unit6": "f",
    "unit7": "k"
    }


"""
    user permissions
    params: addLocation, getMyLocation, getMyLocations, updateLocationUnit, deleteMyLocation
    
    Validation is made custom for each field, city and country_code is required
        while unit and country are optionally
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

    global valid_units

    if city == "":
        message = {"message":'Please insert a city!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    
    elif not city.isalpha():
        message = {"message":'Other characters than strings are not accepted for city!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        city = city.capitalize()

    if country == "":
        country = country
    elif not country.isalpha():
        message = {"message":'Other characters than strings are not accepted for country!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

    if country_code == "":
        message = {"message":"provide country code, e.g. for Ireland is 'ie' "}
        return Response(message, status=status.HTTP_201_CREATED)
    elif not country_code.isalpha():
        message = {"message":'Other characters than strings are not accepted for country code!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    elif not len(str(country_code)) == 2:
        message = {"message":"Country code accepted is 2 letters only, e.g. for Ireland is 'ie' "}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    else:
        country_code = country_code.capitalize()


    if unit in valid_units.values(): 
        unit = unit.lower()
    else:
        message = {"unit can be":'metric: c or celsius | imperial: f or fahrenheit | kelvin: k or kelvin'}
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
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyLocationById(request, pk):
    user = request.user

    try:
        my_city = user.my_locations.get(id=pk)
        if user.is_staff or my_city.user == user:
            serializer = UsersLocationsSerializer(my_city, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this city'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Location does not exist'}, status=status.HTTP_400_BAD_REQUEST)
   

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
    
    global valid_units
     
    if city or country_code or country != "":
        message = {"message": "You cannot to perform this action. Please search another city!"}
        return Response(message, status=status.HTTP_403_FORBIDDEN)
    
    new_units = UsersLocations.objects.filter(user=user)
    new_unit = new_units.get(id=pk) 
    
    
    if user != new_unit:
        message = {"Warning":"You are not the right user to do this!"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)
    
    new_unit.unit=data['unit']
    
    
    if new_unit == "":
        message = message = {"unit can be":'metric: c or celsius | imperial: f or fahrenheit | kelvin: k or kelvin'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)
    elif new_unit not in valid_units.values():
        message = {"unit can be":'metric: c or celsius | imperial: f or fahrenheit | kelvin: k or kelvin'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    else:
        new_unit = new_unit.lower()  
        
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
