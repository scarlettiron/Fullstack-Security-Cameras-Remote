from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/devices/', include('devices.urls')), 
    path('api/alerts/', include('alerts.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
