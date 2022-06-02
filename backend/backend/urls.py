from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('base.urls.user_urls')),
    path('notes/', include('base.urls.notes_urls')),
]
