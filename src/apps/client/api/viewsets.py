
from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.client.models import Client
from apps.client.api.serializers import ClientSerializer, CreateClientSerializer
from apps.client.api.permissions import ClientPermissions
from apps.client.services import ClientUpdator, ClientCreator

from randevu import viewsets
from randevu.pagination import AppPagination
from randevu.validators import PaginationSerializer
from randevu.errors import safe_run
from randevu.viewsets import AppViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ClientViewSet(viewsets.AppViewSet):
    queryset = Client.objects.filter(is_deleted=False)
    lookup_field = 'pkid'
    serializer_class = ClientSerializer
    serializer_action_classes = {
        'retrieve': ClientSerializer,
        'create': CreateClientSerializer,
        'update': CreateClientSerializer,
        'list': ClientSerializer,
    }

    pagination_class = AppPagination
    permission_classes = [
        ClientPermissions
    ]

    def get_queryset(self):
        """Filter clients only for current user company"""
        queryset = super().get_queryset()

        if self.request.user:
            return queryset.for_user(self.request.user)

        return Client.objects.none()

    @swagger_auto_schema(responses={200: openapi.Response('Categories', ClientSerializer(many=True))})
    @action(methods=['GET'], detail=True)
    def list(self, request):
        return super().list(request)

    @swagger_auto_schema(
        responses={200: openapi.Response('Categories', ClientSerializer)}
    )
    @action(methods=['POST'], detail=True)
    @safe_run()
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            client = Client.objects.get(phone=serializer.validated_data['contacts']['phone'], is_deleted=False)
            if client.name != serializer.validated_data['name']:
                serializer = self.get_serializer(client, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @safe_run()
    def update(self, request: Request, *args, **kwargs) -> Response:
        super().update(request, *args, **kwargs)  # type: ignore

        return Response(status=status.HTTP_200_OK)

    @safe_run()
    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        
        if instance.is_deleted == True:
            raise Exception('Client already deleted.')
        instance.is_deleted = True
        instance.save()
        
        return Response(status=204)
    
    def get_object(self) -> Client:
        return super().get_object()
