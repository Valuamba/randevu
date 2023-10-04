from rest_framework.response import Response
from rest_framework.decorators import action

from randevu.viewsets import AppViewSet
from randevu.errors import safe_api

from apps.multilanding.api.serializers import CompanyInfoSerializer,\
    CompanySerializer, MultilandingSerializer, UpdateMultilandingSerializer, SettingsSerializer
from apps.multilanding.models import Multilanding
from apps.multilanding.api.permissions import MultilandingPermissions

from rest_framework import status

from django.conf import settings
from django.apps import apps

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging
import re

logger = logging.getLogger(__name__)


class WebSiteViewSet(AppViewSet):
    serializer_class = MultilandingSerializer
    lookup_field = 'pkid'
    serializer_action_classes = {
        'retrieve': MultilandingSerializer,
        'update': UpdateMultilandingSerializer,
        'update_serializer': SettingsSerializer
    }

    permission_classes = [
        MultilandingPermissions
    ]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            queryset = user.company
        elif f'HTTP_{settings.SFC_ZONE_HEADER}' in self.request.META.keys():
            sub_domain = self.request.META.get(f'HTTP_{settings.SFC_ZONE_HEADER}')
            queryset = Multilanding.objects.get(sub_domain=sub_domain)
        else:
            queryset = Multilanding.objects.all()

        return queryset

    @safe_api
    def retrieve(self, request):
        serializer = MultilandingSerializer(self.get_queryset())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: openapi.Response('Company', CompanySerializer)})
    @action(methods=['GET'], detail=True)
    @safe_api
    def company(self, request):
        multilanding = self.get_queryset()
        serializer = CompanySerializer(data={
            'name': multilanding.name.get(multilanding.default_lang, None),
            'logo': multilanding.logo
        })
        serializer.is_valid(raise_exception=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: openapi.Response('Company info', CompanyInfoSerializer)})
    @action(methods=['GET'], detail=True)
    @safe_api
    def info(self, request):
        multilanding = self.get_queryset()
        serializer = CompanyInfoSerializer(data={
            'pkid': multilanding.pkid,
            'logo': multilanding.logo,
            'name': multilanding.name.get(multilanding.default_lang, None),
            'subdomain': multilanding.sub_domain
        })
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: openapi.Response('Retrieve settings', SettingsSerializer)})
    @action(methods=['GET'], detail=True)
    @safe_api
    def retrieve_settings(self, request) -> Response:
        multilanding = self.get_queryset()
        serializer = SettingsSerializer(multilanding)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update staff schedule", 
        request_body=SettingsSerializer)
    @action(methods=['PUT'], detail=True)
    @safe_api
    def update_settings(self, request):
        multilanding = self.get_queryset()

        serializer = SettingsSerializer(multilanding, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(status=status.HTTP_200_OK)

    def get_object(self):
        return self.get_queryset()