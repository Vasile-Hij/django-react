from django.urls import path
from base.views import location_views as views


urlpatterns = [
    path('admin', views.getCities, name='All cities'),
    
    path('', views.getMyCities, name='My cities'),
    path('add/', views.addCity, name='Create city'),
    path('city/', views.getMyCity, name='My city'),
    path('update/', views.updateCity, name='Update city'),
    path('delete/', views.deleteCity, name='Delete city')
]
