from django.urls import path
from base.views import notes_views as views


urlpatterns = [
    path('', views.getNotes),
]