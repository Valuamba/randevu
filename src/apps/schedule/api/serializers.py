from rest_framework import serializers

from apps.schedule.models import StaffBreak, StaffSchedule
from randevu import validators


class StaffBreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffBreak
        fields = [
           'start_break_time_step',
           'end_break_time_step'
        ]
        

class StaffScheduleSerializer(serializers.ModelSerializer):
    breaks = StaffBreakSerializer(many=True, read_only=True)

    class Meta:
        model = StaffSchedule
        fields = [
            'week_day',
            'start_work_time_step',
            'end_work_time_step',
            'is_day_off',
            'breaks'
        ]