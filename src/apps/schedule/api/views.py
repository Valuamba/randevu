from wsgiref.validate import validator
from django.shortcuts import get_list_or_404, get_object_or_404, render

from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.schedule.api.serializers import StaffScheduleSerializer
from apps.schedule.services import WeeklyScheduleUpdater
from apps.schedule.api.validators import StaffScheduleValidator
from apps.schedule.api.permissions import StaffSchedulePermissions
from apps.users.models.user import User
from randevu.views import AnonymousAPIView, AuthenticatedAPIView
from randevu.viewsets import ValidationMixin

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from randevu.errors import safe_api


class StaffScheduleAPIView(AnonymousAPIView, ValidationMixin):
    validator_class = StaffScheduleValidator

    permission_classes = [
        StaffSchedulePermissions
    ]
    
    @swagger_auto_schema(
        operation_description="Update staff schedule", 
        request_body=StaffScheduleValidator)
    @safe_api
    def put(self, request, employee_id):
        self.data = request.data
        self.data['employee_id'] = employee_id
        
        self._validate(self.data)
        
        self.update_schedule()
        
        return Response({'ok': True, 'message': 'Schedule was updated successfully.'}, status=201)

    def _get_user(self):
        return get_object_or_404(User, pkid=self.data.get('employee_id'))
    
    def update_schedule(self):
        WeeklyScheduleUpdater(
            user=self._get_user(),
            weekly_schedule_data=self.data.get('schedule')
        )()

        
        
