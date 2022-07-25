from django.contrib import admin
from .models import Note, Location, UsersLocations, \
    ForecastHourly, ForecastNow

admin.site.register(Note)
admin.site.register(Location)
admin.site.register(UsersLocations)
admin.site.register(ForecastHourly)
admin.site.register(ForecastNow)


