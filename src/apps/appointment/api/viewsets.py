from randevu import viewsets

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import filters

from apps.users.models import User
from apps.service.models import Category, SalonService
from apps.client.models import Client

from apps.appointment.models import Appointment
from apps.appointment.api.serializers import AppointmentSerializer, CreateAppointmentSerializer,\
    AppointmentFilterSerializer, AppointmentParametersSerializer
from apps.appointment.api.permissions import AppointmentPermissions
from apps.appointment.services import AppointmentCreator, AppointmentUpdator
from apps.client.services import ClientCreator, ClientUpdator

from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

from django.utils import timezone
import zoneinfo

from randevu.errors import safe_api

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from enum import IntEnum

from randevu.pagination import AppPagination

logger = logging.getLogger(__name__)


class AppointmentViewSet(viewsets.AppViewSet):
    queryset = Appointment.objects.filter(is_deleted=False)
    lookup_field = 'pkid'
    serializer_class = AppointmentSerializer
    serializer_action_classes = {
        'create': CreateAppointmentSerializer,
        'update': CreateAppointmentSerializer,
        'list': AppointmentFilterSerializer
    }
    filter_backends = [filters.SearchFilter]
    search_fields = ['client__name', 'client__phone']

    pagination_class = AppPagination
    permission_classes = [
        AppointmentPermissions
    ]

    def get_queryset(self):
        """Filter appointments only for current user"""
        queryset = super().get_queryset()

        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)

        employee = self.request.query_params.get('employee')
        if employee is not None:
            queryset = queryset.filter(employee=employee)

        interval = self.request.query_params.get('interval')
        if interval:
            if int(interval) == Appointment.TODAY:
                queryset = queryset.filter(day__day=timezone.now().day)
            elif int(interval) == Appointment.MONTH:
                queryset = queryset.filter(day__month=timezone.now().month)
            else:
                raise Exception('Incorrect interval.')

        client_pkid = self.request.query_params.get('client_pkid')
        if client_pkid is not None:
            queryset = queryset.filter(client=client_pkid)

        if self.request.user:
            return queryset.for_user(self.request.user)

        return Appointment.objects.none()

    @swagger_auto_schema(
        query_serializer=AppointmentParametersSerializer,
        responses={200: openapi.Response('Appointments', AppointmentSerializer)})
    def list(self, request):
        serialzier = AppointmentSerializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response(data=serialzier.data, status=status.HTTP_200_OK)

    @atomic
    @safe_api
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = CreateAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        client = self.create_or_update_client(data.pop('client'), user.company)
        self.create_appointment(
            client=client, 
            service_id = data['service']['id'],
            category_id = data['category']['id'],
            employee_id = data['employee']['id'],
            day = data['date']['day'],
            time_step = data['date']['time_step'],
            company = user.company
        )
        
        return Response(status=status.HTTP_201_CREATED)  

    @atomic
    @safe_api
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = CreateAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        appointment = self.get_object()

        client = self.create_or_update_client(data.pop('client'), user.company)
        self.update_appointment(
            appointment=appointment, 
            client=client, 
            service_id = data['service']['id'],
            category_id = data['category']['id'],
            employee_id = data['employee']['id'],
            day = data['date']['day'],
            time_step = data['date']['time_step']
            )
        
        return Response(status=status.HTTP_200_OK)  

    def update_appointment(self, appointment: Appointment, service_id: int, employee_id: int, category_id: int, client: Client, day: str, time_step: int):
        return AppointmentUpdator(
            appointment=appointment,
            service=SalonService.objects.get(pkid=service_id),
            employee=User.objects.get(pkid=employee_id),
            category=Category.objects.get(pkid=category_id),
            client=client,
            date=day,
            time_step=time_step
        )()

    def create_appointment(self, company, service_id: int, employee_id: int, category_id: int, client: Client, day: str, time_step: int) -> Appointment:
        return AppointmentCreator(
            service=SalonService.objects.get(pkid=service_id),
            employee=User.objects.get(pkid=employee_id),
            category=Category.objects.get(pkid=category_id),
            client=client,
            day=day,
            time_step=time_step,
            company = company
        )()

    def create_or_update_client(self, client_data: dict, company):
        try:
            client = Client.objects.get(phone=client_data['phone'], is_deleted=False)
            if client.name != client_data['name']:
                client = ClientUpdator(client, **client_data)()
        except Client.DoesNotExist:
            client = ClientCreator(**client_data, company=company)()
        return client

    @safe_api
    def cancel(self, request):
        instance = self.get_object()
        instance.status = Appointment.CANCELED
        instance.save()
        return Response(status=200)

    @safe_api
    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        
        if instance.is_deleted == True:
            raise Exception('Appointment already deleted.')
        instance.is_deleted = True
        instance.save()
        
        return Response(status=204)
    
    def get_object(self) -> Appointment:
        return super().get_object()