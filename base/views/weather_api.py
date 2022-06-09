#!/bin/usr/env python3
import datetime
import json
import pprint
import urllib.parse
from configparser import ConfigParser

import requests

# reading varialbles
config = ConfigParser()
config.read('.settings.ini')


 # connection to Open Weather    
BASE_WEATHER_API_URL = f'http://api.openweathermap.org/data/2.5/onecall/timemachine?'
WEATHER_API_KEY = config.get('weather_api', 'WEATHER_API_KEY')

# connection to google geolocation
BASE_GOOGLE_URL = f'https://maps.googleapis.com/maps/api/geocode/json?'
GOOGLE_GEOLOCATION_API=config.get('google_api', 'GOOGLE_GEOLOCATION_API')

# fetchGoogleLocationCity
city_name = 'Bucharest'

# fetchGoogleLocationStreet 
street_address = 'Benjamin Franklin 1, Bucharest' # google is sorting the input for now, other example e.g: 1 Franklin Bucharest
components = '' # short country code can be used if two cities have same name e.g: London, US

# standard is imperial by default
units = 'standard'

def getUTCNow():
    return int(datetime.datetime.utcnow().timestamp())


def fetchGoogleLocationCity():
    custom_google_api = {
    'address': city_name,
    'key': GOOGLE_GEOLOCATION_API
    }
    
    url = BASE_GOOGLE_URL + urllib.parse.urlencode(custom_google_api)
    
    long_response =  requests.get(url).json()
    response = long_response['results'][0]['geometry']['location']
    lat = response['lat']
    lon = response['lng']
    
    return lat, lon
    
    
def fetchGoogleLocationStreet():
    custom_google_api = {
    'address': street_address,
    'components': components,
    'key': GOOGLE_GEOLOCATION_API
    }
    
    url = BASE_GOOGLE_URL + urllib.parse.urlencode(custom_google_api)
    
    long_response =  requests.get(url).json()
    response = long_response['results'][0]['geometry']['location']
    lat = response['lat']
    lon = response['lng']
    
    return lat, lon    
    

def fetchWeatherApi():
    today = getUTCNow()
    # past24h = getUTCNow() - (24 * 60 * 60) # the api I used already have past 24h
    
    try:
        lat, lon = fetchGoogleLocationCity()
    except:
        return "Please insert city name or street address"
    else:
        lat, lon = fetchGoogleLocationStreet()
    
    custom_weather_api = {
        'lat': lat,
        'lon': lon,
        'dt': today,
        'units':units, 
        'appid': WEATHER_API_KEY
        }
    
    
    url = BASE_WEATHER_API_URL + urllib.parse.urlencode(custom_weather_api)
    
    long_response = requests.get(url).json()
    response = long_response['current']
    return response
    


#pprint.pprint(fetchGoogleLocationCity())
pprint.pprint(f'Retreive latitude and longitude from hardcoded adress: {fetchGoogleLocationStreet()}')
print('-------------------')
pprint.pprint(f'Fetched data as address input: {fetchWeatherApi()}')
