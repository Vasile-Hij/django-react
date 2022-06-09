#!/bin/usr/env python3
import datetime
import json
import urllib.parse
from configparser import ConfigParser

import requests

config = ConfigParser()
config.read('.settings.ini')

    
BASE_WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?'
WEATHER_API_KEY = config.get('weather_api', 'WEATHER_API_KEY')

lat = '44.439663'
lon = '26.096306'
units = 'standard'



def getUTCNow():
    return int(datetime.datetime.utcnow().timestamp())


def fetchWeatherApi():
    today = getUTCNow()
    past24h = getUTCNow() - (24 * 60 * 60)

    CUSTOM_WEATHER_API = {
        'lat':lat,
        'lon':lon,
        'dt':today,
        'units':units, 
        'appid': WEATHER_API_KEY
        }
    
    
    URL = BASE_WEATHER_API_URL + urllib.parse.urlencode(CUSTOM_WEATHER_API)
    return requests.get(URL).json()

print(fetchWeatherApi())
