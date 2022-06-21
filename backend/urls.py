from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('base.urls.user_urls')),
    path('notes/', include('base.urls.notes_urls')),
    path('weather/', include('base.urls.weather_urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)