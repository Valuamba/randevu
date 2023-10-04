from typing import Any

from apps.schedule.models import StaffSchedule

from rest_framework import serializers
from randevu import validators

from django.conf import settings


class WorkDayUpdaterSerializer(serializers.ModelSerializer):
    start_work_time_step = serializers.IntegerField(required=True, allow_null=False)
    end_work_time_step = serializers.IntegerField(required=True, allow_null=False)
    
    class Meta:
        model = StaffSchedule
        fields = [
            'start_work_time_step',
            'end_work_time_step'
        ]
        
    
class WorkDayUpdater:
    def __init__(self, daily_schedule: StaffSchedule, day_data: dict) -> None:
        self.daily_schedule = daily_schedule
        self.day_data = day_data
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        daily_schedule = self.daily_schedule
        breaks = self.day_data.pop('breaks', [])
        
        self.validate(daily_schedule)
        
        self.update(daily_schedule)
        daily_schedule.refresh_from_db()
        
        daily_schedule.reset_breaks()
        daily_schedule.set_breaks(breaks)
        
    def validate(self, day: StaffSchedule):
        if day.is_day_off:
            raise validators.ValidationError('You cannot update day off.')
        
    def validate_update_data(self, start_work_time_step, end_work_time_step):
        if start_work_time_step >= end_work_time_step:
            raise validators.ValidationError('End time step must be greater than start time step.')

        if end_work_time_step > settings.MAX_TIME_STEPS:
            raise validators.ValidationError(f'Time step cannot exceed the max number of time steps per a day {settings.MAX_TIME_STEPS}')    
    
    
    def update(self, daily_schedule: StaffSchedule):
        serializer = WorkDayUpdaterSerializer(instance=daily_schedule, data=self.day_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.validate_update_data(**serializer.validated_data)
        
        serializer.save()        