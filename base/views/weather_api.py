#!/bin/usr/env python3
import requests
import logging
import urllib.parse
import pycountry

from configparser import ConfigParser

logger = logging.getLogger(__name__)

# reading varialbles
config = ConfigParser()
config.read('.settings.ini')


 # connection to Open Weather    
BASE_WEATHER_API_URL = f'https://api.openweathermap.org/data/2.5/'
WEATHER_API_KEY = config.get('weather_api', 'WEATHER_API_KEY')


class LocationApi(object):
    def __init__(self, api=BASE_WEATHER_API_URL, api_key=WEATHER_API_KEY ):
        self.api = api
        self.api_key = api_key

    def _add_unit_and_api_key(self, url, unit):
        """
            Adds unit and api key to the url of OpenWeatherMap API.
            :param url: Base address to the OpenWeatherMap api
            :param unit: Temperature unit of either C, F or K.
            :return: Tuple of the url and determined unit
        """
        unit = unit.lower()
    
        if unit == 'c' or unit == 'celsius':
            unit_url = "&units=metric"
            unit = '°C'
        elif unit == 'f' or unit == 'fahrenheit':
            unit_url = '&units=metric'
            unit = '°F'
        elif unit == 'k' or unit == 'kelvin':
            unit_url = 'kelvin'
            unit = 'K'
        else:
            raise TypeError('Always provide unit')
        

        url = self.api + unit_url + '&appid={}'.format(self.api_key) 
        logger.debug(f'Complete URL to API: {str(url)}')
        return url, unit
        
        
    def current_location_weather(self, location, unit=None):
        """
            Request weather by location from Open Weather Map
            :param location: Location in format of: {city name},{country code}, but country code is not required,
            however it needs to be supplied in ISO 3166 format (e.g. ro, uk, etc.) if it was given. Example location: "Bucharest, ro"
            :param unit: Temperature unit (e.g. C, F, K, full names also work). Defaults to Celsius.
            :return: Weather data as dictionary.
        """

        
        location = self.check_country_code(location)

        if unit is None:
            logger.debug(f'Temperature unit is missing; default is metric')
            unit = 'c'

        url = self.api + 'weather?q={}'.format(location)
        complete_url, unit = self._add_unit_and_api_key(url, unit)
        response = requests.get(url=complete_url)
        data = response.json()


        logger.debug(f'Received weather data: {str(data)}')

        country_code = data['sys']['country']
        
        weather_data = {
            # Location details
            'id': data['id'],
            'city': data['name'],
            'country_code': data['sys']['country'],
            'country': self.country_code_to_country(country_code),
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon'],
            # Temperature details
            'temperature': data['main']['temp'],
            'temperature_max': data['main']['temp_max'],
            'temperature_min': data['main']['temp_min'],
            'temparature_unit': unit,
            # Other weather details
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }

        logger.debug(f'Fetched data to: {str(weather_data)}')

        return weather_data


    @staticmethod
    def check_country_code(location):
        """In case country was given, it will get shortened from Romania to ro.
        :param location: in format of: {city name},{country code}, but country code is not required
        :return: location
        """
        city_and_country = location.split(',', 1)

        if len(city_and_country) is not 2:
            logger.debug(f'No country code were given')
            logger.debug(f'Location code is {location}')
            return location

        city = city_and_country[0]
        country = city_and_country[1]
        logger.debug(f'Country code is {country}')

        if country != '':
            logger.debug(f'Converting {country} to country code')
            country_code = pycountry.countries.get(name=country).alpha_2.lower()
            logger.debug(f'Country code is {country_code}')
            location = city + ',' + country_code
            logger.debug(f'Location is {location}')
        else:
            location = city
        
        return location


    @staticmethod
    def country_code_to_country(country_code):
        return pycountry.countries.get(alpha_2=country_code).name


    @staticmethod
    def check_location(location):
        city_and_country = location.rsplit(',', 1)
        city = city_and_country[0]

        # Converting diacritical characters to English chraracters  
        city_to_english_alphabet = city.replace('ă', 'a').replace('â', 'a').replace('ș', 's').replace('ț','t')

        if len(city_and_country) is not 2:
            logger.debug(f'No country code was given')
        else: 
            country_code = city_and_country[1]
            logger.debug(f'Country code is {country_code}')
            city_to_english_alphabet =  city_to_english_alphabet  + ',' + country_code

        logger.debug(f'Location is {city_to_english_alphabet}')
        return city_to_english_alphabet