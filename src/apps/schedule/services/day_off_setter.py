from typing import Any

from uritemplate import partial
from randevu import validators
from apps.schedule.models import StaffSchedule

from rest_framework import serializers


class DayOffScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSchedule
        fields = [
            'start_work_time_step',
            'end_work_time_step',
            'is_day_off'
        ]
    
    
class DayOffScheduleSetter:
    def __init__(self, daily_schedule: StaffSchedule) -> None:
        self.daily_schedule = daily_schedule
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        daily_schedule = self.daily_schedule
        
        self.validate(daily_schedule)
        self.update(daily_schedule)
        daily_schedule.refresh_from_db()
        
        daily_schedule.reset_breaks()
    
    def validate(self, daily_schedule: StaffSchedule):
        if daily_schedule.is_day_off == True:
            raise validators.ValidationError('Day is already day off.')
    
    def update(self, daily_schedule: StaffSchedule):
        serializer = DayOffScheduleUpdateSerializer(
            instance=daily_schedule,
            data={
                'start_work_time_step': None,
                'end_work_time_step': None,
                'is_day_off': True
            },
            partial = True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()