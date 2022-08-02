from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(User,
                             related_name='notes',
                             on_delete=models.CASCADE,
                             null=True)
    body = models.TextField()


class Location(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ManyToManyField(User, 
                            through='UsersLocations')
    city = models.CharField(max_length=85)
    country = models.CharField(max_length=85, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=4,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=4,
                                    null=True, blank=True)
    zip_code = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.city}, {self.country_code}'
    
    class Meta: 
        verbose_name_plural = 'Locations'
        unique_together = [("city", "country_code")]


class UsersLocations(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, 
                            on_delete=models.CASCADE,
                            related_name='my_locations',
                            null=True)
    location_city = models.ForeignKey(Location,
                            on_delete=models.CASCADE,
                            related_name='location_city',
                            null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user}, {self.location_city}' 
    
    class Meta:
        verbose_name = 'userlocation'
        unique_together = [('user', 'location_city')]


class ForecastHourly(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    city = models.CharField(max_length=85)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    feels_like = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    temperature_unit = models.CharField(max_length=10, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pressure = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    description = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'{self.id},{self.city}'
    
    
class ForecastNow(models.Model):
    city = models.CharField(max_length=85)
    country_code = models.CharField(max_length=3, blank=True)
    country = models.CharField(max_length=50, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    temperature_unit = models.CharField(max_length=10, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pressure = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    description = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'{self.city}'
