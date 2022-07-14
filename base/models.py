from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(User,
                             related_name='user_notes',
                             on_delete=models.CASCADE,
                             null=True)
    body = models.TextField()


class City(models.Model):
    userTag = models.ManyToManyField(User, 
                                  through='UsersLocations',
                                  through_fields=('city', 'user'),
                                  related_name="user_search_cities",
                                  blank=True)
    id = models.AutoField(primary_key=True, editable=False)
    location = models.CharField(max_length=85)
    country = models.CharField(max_length=85, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=4,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=4,
                                    null=True, blank=True)
    zip_code = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.location}, {self.country_code}'
    
    class Meta: 
        verbose_name_plural = 'cities'
        unique_together = ("location", "country_code")


class UsersLocations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City,
                             on_delete=models.CASCADE,
                             related_name='locations_by_users',
                             null=True)
    id = models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return f'{self.user}, {self.city}'
    
    class Meta:
        unique_together = [['user', 'city']]
        