from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User
from apps.service.models import SalonService
from apps.employee.api.serializers import CalculateEmployeeFreeTimeSlotsSerualizer, EmployeeWorkTimeSerializer
from apps.employee.services import EmployeeMonthTimeSlots
from apps.employee.api.permissions import EmployeePermissions

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q

from randevu.errors import safe_api


employee_time_response = openapi.Response('Free slots', EmployeeWorkTimeSerializer)


class CalculateFreeEmployeeTimeSlotsAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CalculateEmployeeFreeTimeSlotsSerualizer

    def get_queryset(self):
        zone = self.request.META.get(f'HTTP_{settings.SFC_ZONE_HEADER}', None)
        if self.request.user.is_authenticated:
            user = self.request.user
            query = Q(company=user.company) & Q(role__in=[User.EMPLOYEE, User.ADMIN]) & ~Q(status=User.REMOVED)

            return User.objects.filter(query)
        elif zone:
            query = Q(company__sub_domain=zone) & Q(role__in=[User.EMPLOYEE, User.ADMIN]) & ~Q(status=User.REMOVED)
            return User.objects.filter(query)

        return User.objects.none()

    @swagger_auto_schema(
        operation_description="Calculate employee free time slots", 
        responses={200: employee_time_response})
    @safe_api
    def post(self, request):
        data = request.data
        serializer = CalculateEmployeeFreeTimeSlotsSerualizer(data=data)
        serializer.is_valid(raise_exception=True)

        service_id = serializer.validated_data.pop('service_id', None)

        user = get_object_or_404(self.get_queryset(), pkid=serializer.validated_data['employee_id'])
        
        service = None
        if service_id:
            service = SalonService.objects.get(pkid=service_id, company=user.company)

        time_slots = EmployeeMonthTimeSlots(user, year=serializer.validated_data['year'],
            month=serializer.validated_data['month'], service=service)()

        response_serializer = EmployeeWorkTimeSerializer(data=time_slots)
        response_serializer.is_valid(raise_exception=True)

        return Response(data=response_serializer.validated_data, status=status.HTTP_200_OK)
