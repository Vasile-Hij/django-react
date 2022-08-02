from django.urls import path
from base.views import location_views as views
from base.views import forecast_views as forecast_views


urlpatterns = [
    path('cities/', views.getMyLocations, name='my-cities'),
    path('add/', views.addLocation, name='create-city'),
    path('update/<str:pk>/', views.updateLocationUnit, name='my-location-unit'),
    path('city/<str:pk>/', views.getMyLocationById, name='my-location'),
    path('delete/<str:pk>/', views.deleteMyLocation, 
         name='delete-my-location'),
    
    path('city/<str:pk>/forecast/now/', forecast_views.weatherNow, name='forecast-now'),
]
