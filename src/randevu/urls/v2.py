"""vpn-admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("openapi-schema/", get_schema_view(), name="openapi-schema"),
    path('auth/', include('apps.users.urls')),
    # path('locales/', include('apps.locales.urls')),

    path('', include('apps.cloudfare.urls')),
    path('', include('apps.multilanding.urls')), 
    path('', include('apps.client.urls')),
    path('', include('apps.appointment.urls')),
    path('', include('apps.schedule.urls')),
    path('', include('apps.service.urls')),
    path('', include('apps.employee.urls')),
    path('', include('apps.schedule.urls'))
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
