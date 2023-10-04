from django.urls import path, include

from rest_framework.routers import SimpleRouter

from apps.service.api.viewsets import CategoryViewSet, ServiceViewSet

router = SimpleRouter()


open_urls = [
    path('open/services/', ServiceViewSet.as_view({'get': 'list'})),
]

urlpatterns = [
    path('categories/', CategoryViewSet.as_view({'get': 'list'}), name='list-cetegories'),
    path('category/<str:pkid>/update', CategoryViewSet.as_view({'put': 'update'})),
    path('category/<str:pkid>/delete', CategoryViewSet.as_view({'delete': 'destroy'})),
    path('category/create', CategoryViewSet.as_view({'post': 'create'})),

    path('services/', ServiceViewSet.as_view({'get': 'list'})),
    path('service/<str:pkid>/update', ServiceViewSet.as_view({'put': 'update'})),
    path('service/<str:pkid>/delete', ServiceViewSet.as_view({'delete': 'destroy'})),
    path('service/create', ServiceViewSet.as_view({'post': 'create'})),    
] + open_urls