import logging

from django.db.transaction import atomic
from django.conf import settings

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from apps.users.models.user import User
from apps.employee.api import serializers
from apps.employee.api.permissions import EmployeePermissions

from randevu.viewsets import AppViewSet
from randevu.errors import safe_api

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger()


service_id = openapi.Parameter('service_id', openapi.IN_QUERY, description="Service", type=openapi.TYPE_STRING)


class EmployeeViewSet(AppViewSet):
    queryset = User.objects.for_employee_viewset()
    lookup_field = "pkid"
    serializer_class = serializers.EmployeeSerialzer
    serializer_action_classes = {
        'create': serializers.EmployeeCreateSerializer,
        'update': serializers.EmployeeUpdateSerializer,
        'retrieve': serializers.EmployeeSerialzer
    }

    permission_classes = [
        EmployeePermissions
    ]

    @safe_api
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        zone = self.request.META.get(f'HTTP_{settings.SFC_ZONE_HEADER}', None)
        if self.request.user and not self.request.user.is_anonymous:
            return User.objects.for_user(self.request.user)
        elif self.action == 'list' and zone: 
            return User.objects.for_zone(zone)

        return User.objects.none()
    
    @safe_api
    @swagger_auto_schema(manual_parameters=[service_id])
    def list(self, request):
        service_id = request.GET.get('service_id', None)

        if service_id:
            users = self.get_queryset().filter(service_id=service_id).all()
        else:
            users = self.get_queryset().all()

        serializer = serializers.EmployeeSerialzer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @atomic
    @safe_api
    def create(self, request: Request, *args, **kwargs) -> Response:
        response = super().create(request, *args, **kwargs)  # type: ignore
        if response.status_code not in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            return response

        self.kwargs[self.lookup_field] = response.data.get('pkid')
        answer = self.get_object()
        answer.refresh_from_db()
        
        answer.set_schedule()

        return Response(data={
            'pkid': answer.pkid
        }, status=status.HTTP_201_CREATED)

    @safe_api
    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        
        if instance.status == User.REMOVED:
            raise Exception('User already deleted.')
        instance.status = User.REMOVED
        instance.save()
        
        return Response(status=204)
    
    def get_object(self) -> User:
        return self.get_queryset().get(pkid=self.kwargs[self.lookup_field])

    