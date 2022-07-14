from django.contrib import admin
from .models import Note, City, UsersLocations

admin.site.register(Note)
admin.site.register(City)
admin.site.register(UsersLocations)

