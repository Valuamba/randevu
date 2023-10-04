import logging
from rest_framework import serializers
from apps.schedule.api.serializers import StaffScheduleSerializer

from apps.users.models import User


logger = logging.getLogger()


class EmployeeSerialzer(serializers.ModelSerializer):
    from apps.service.api.serializers import SalonServiceSerializer

    weekly_schedule = StaffScheduleSerializer(many=True)
    services = SalonServiceSerializer(many=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'pkid',
            'name',
            'is_owner',
            'phone',
            'email',
            'status',
            'role',
            'image',
            'thumb_image',
            'weekly_schedule',
            'services'
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    pkid = serializers.IntegerField(read_only=True)
    role = serializers.ChoiceField(choices=User.EMPLOYEE_CREATE_ROLES)
    status = serializers.ChoiceField(choices=User.EMPLOYEE_CREATE_STATUS)

    class Meta:
        model = User
        fields = [
            'pkid',
            'name',
            'phone',
            'email',
            'status',
            'role',
            'image',
            'thumb_image',
            'services',
        ]
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['company'] = user.company
        return super().create(validated_data)

        
class EmployeeUpdateSerializer(serializers.ModelSerializer): 
    role = serializers.ChoiceField(choices=User.EMPLOYEE_CREATE_ROLES)

    class Meta:
        model = User
        fields = [
            'name',
            'phone',
            'status',
            'email',
            'role',
            'services',
            'image',
            'thumb_image'
        ]


class EmployeeTimeSlotSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    label = serializers.CharField()


class WorkTimeOfDaySerializer(serializers.Serializer):
    free_time_slots = serializers.ListField(child=EmployeeTimeSlotSerializer(required=False))
    status = serializers.BooleanField()


class EmployeeWorkTimeSerializer(serializers.Serializer):
    days = serializers.DictField(child=WorkTimeOfDaySerializer())


class CalculateEmployeeFreeTimeSlotsSerualizer(serializers.Serializer):
    service_id = serializers.IntegerField(required=False)
    employee_id = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()