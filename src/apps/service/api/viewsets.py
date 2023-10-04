
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import action

from apps.service.api.serializers import CategoryCreateSerializer, CategorySerializer,\
     SalonServiceCreateSerializer, SalonServiceSerializer
from apps.service.models import Category, SalonService
from apps.locales.models import MultilandingLocale
from apps.service.api.permissions import ServicePermissions, CategoryPermissions

from randevu.viewsets import AppViewSet
from randevu.errors import safe_api
from randevu.validators import PaginationSerializer
from randevu.pagination import AppPagination

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.conf import settings


category_id = openapi.Parameter('category_id', openapi.IN_QUERY, description="Category", type=openapi.TYPE_STRING)


class CategoryViewSet(AppViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    lookup_field = 'pkid'
    serializer_action_classes = {
        'create': CategoryCreateSerializer,
        'update': CategoryCreateSerializer,
        'categories': PaginationSerializer
    }

    pagination_class = AppPagination
    permission_classes = [
        CategoryPermissions
    ]

    @swagger_auto_schema(responses={200: openapi.Response('Categories', CategorySerializer(many=True))})
    @action(methods=['GET'], detail=True)
    def list(self, request):
        return super().list(request)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            return queryset.for_user(self.request.user)

        return Category.objects.none()

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
    @safe_api
    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=204)
    
    def get_object(self) -> Category:
        return Category.objects.get(pkid=self.kwargs[self.lookup_field])
    
    
class ServiceViewSet(AppViewSet):
    queryset = SalonService.objects.filter(is_deleted=False)
    serializer_class = SalonServiceSerializer
    lookup_field = 'pkid'
    serializer_action_classes = {
        'create': SalonServiceCreateSerializer,
        'update': SalonServiceCreateSerializer,
        'retrieve': SalonServiceSerializer
    }

    permission_classes = [
        ServicePermissions
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        zone = self.request.META.get(f'HTTP_{settings.SFC_ZONE_HEADER}', None)

        if self.request.user.is_authenticated:
            return queryset.for_user(self.request.user)
        elif self.action =='list' and zone:
            return queryset.for_zone(zone)
            
        return SalonService.objects.none()

    @safe_api
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)  # type: ignore
        if response.status_code not in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            return response

        self.kwargs[self.lookup_field] = response.data.get('pkid')
        
        service = self.get_object()
        service.refresh_from_db()
        service.company = request.user.company

        serializer = SalonServiceSerializer(service)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @safe_api
    @swagger_auto_schema(manual_parameters=[category_id])
    def list(self, request):
        category_id = request.GET.get('category_id', None)
        
        if category_id:
            services = self.get_queryset().filter(category_id=category_id).all()
        else:
            services = self.get_queryset().all()

        serializer = SalonServiceSerializer(services, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @safe_api
    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()

        instance.is_deleted = True
        instance.save()
        
        return Response(status=204)
    
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
    def get_object(self) -> SalonService:
        return SalonService.objects.get(pkid=self.kwargs[self.lookup_field])