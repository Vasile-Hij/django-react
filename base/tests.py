from django.test import TestCase
from base.views.weather_api import LocationApiService as locationApiService

# Create your tests here.
url = 'https://api.openweathermap.org/data/2.5/weather?'
unit_url = 'c'
location = 'Bucharest'
country_code = '' # partial_location is no country code


key_and_unit = locationApiService()
test_one = key_and_unit._add_unit_and_api_key(url, unit_url)
# print(f'Testing "add_unit_and_api_key" {test_one}')

partial_location = locationApiService()
test_two = partial_location.current_location_weather(location, unit_url )
print(f'Testing "current_location_weather" {test_two }')

