
from django.urls import path, include
from apps.appointment.api.viewsets import AppointmentViewSet

from rest_framework.routers import SimpleRouter


urlpatterns = [
    path('appointments/', AppointmentViewSet.as_view({'get': 'list'})),
    path('appointment/<str:pkid>/', AppointmentViewSet.as_view({'get': 'retrieve'})),
    path('appointment/<str:pkid>/update', AppointmentViewSet.as_view({'put': 'update'})),
    path('appointment/<str:pkid>/delete', AppointmentViewSet.as_view({'delete': 'destroy'})),
    path('appointment/<str:pkid>/cancel', AppointmentViewSet.as_view({'delete': 'cancel'})),
    path('appointment/create', AppointmentViewSet.as_view({'post': 'create'})),
]