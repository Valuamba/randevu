from apps.schedule.models import StaffSchedule
from typing import Any
from randevu import validators

from django.conf import settings

from rest_framework import serializers


class WorkDayScheduleUpdateSerializer(serializers.ModelSerializer):
    start_work_time_step = serializers.IntegerField(required=True, allow_null=False)
    end_work_time_step = serializers.IntegerField(required=True, allow_null=False)
    
    class Meta:
        model = StaffSchedule
        fields = [
            'start_work_time_step',
            'end_work_time_step',
            'is_day_off'
        ]


class WorkDaySetter:
    def __init__(self, daily_schedule: StaffSchedule, update_data: dict) -> None:
        self.daily_schedule = daily_schedule
        self.update_data = update_data
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        daily_schedule = self.daily_schedule
        breaks = self.update_data.pop('breaks', [])
        
        self.validate(daily_schedule)
        self.update(daily_schedule)
        daily_schedule.refresh_from_db()
        
        daily_schedule.reset_breaks()
        daily_schedule.set_breaks(breaks)
        
    def validate(self, day: StaffSchedule):
        if not day.is_day_off:
            raise validators.ValidationError('You cannot say already work day to work day.')
        
    def validate_update_data(self, start_work_time_step, end_work_time_step, is_day_off):
        if start_work_time_step >= end_work_time_step:
            raise validators.ValidationError('End time step must be greater than start time step.')

        if end_work_time_step > settings.MAX_TIME_STEPS:
            raise validators.ValidationError(f'Time step cannot exceed the max number of time steps per a day {settings.MAX_TIME_STEPS}')

    def update(self, daily_schedule: StaffSchedule):
        serializer = WorkDayScheduleUpdateSerializer(
            instance=daily_schedule,
            data={
                **self.update_data,
                'is_day_off': False
            })
        serializer.is_valid(raise_exception=True)
        self.validate_update_data(**serializer.validated_data)

        serializer.save()
