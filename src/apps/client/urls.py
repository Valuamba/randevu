from django.urls import include, path

from apps.client.api.viewsets import ClientViewSet


urlpatterns = [
    path('clients/', ClientViewSet.as_view({'get': 'list'})),
    path('client/<str:pkid>/', ClientViewSet.as_view({'get': 'retrieve'})),
    path('client/<str:pkid>/update', ClientViewSet.as_view({'put': 'update'})),
    path('client/<str:pkid>/delete', ClientViewSet.as_view({'delete': 'destroy'})),
    path('client/create', ClientViewSet.as_view({'post': 'create'})),
]