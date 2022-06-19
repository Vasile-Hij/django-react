from django.test import TestCase
from base.views.weather_api import LocationApi as locationApi

# Create your tests here.
url = ''
unit_url = 'c'
location = 'Bucharest'
country_code = ''


key_and_unit = locationApi()
test_one = key_and_unit._add_unit_and_api_key(url, unit_url)
print(f'Testing "add_unit_and_api_key" {test_one}')

partial_location = locationApi()
test_two = partial_location.current_location_weather(location, unit_url )
print(f'Testing "current_location_weather" {test_two }')


