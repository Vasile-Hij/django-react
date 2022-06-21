from django.urls import path
from base.views import weather_views as views


urlpatterns = [
 
    path('location/', views.CityListAPIView.as_view()),
    path('location/create/', views.CityListCreate.as_view()),
    path('location/cities/<pk>', views.CityRetrieveUpdateDestroyAPIView.as_view()),
    path('location/city/', views.CityWeather.as_view()),
    path('location/cities/', views.CitiesWeather.as_view()),
]
