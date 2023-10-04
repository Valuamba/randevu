from typing import Any, List

from apps.schedule.models import StaffBreak, StaffSchedule
from rest_framework import serializers

from randevu import validators
from randevu.intersect import Interval, is_intersect, is_intersect_with  


class DailyBreaksCreator:
    def __init__(self, daily_schedule: StaffSchedule, breaks: List[dict]) -> None:
        self.daily_schedule = daily_schedule
        self.breaks = breaks
    
    def __call__(self, *args: Any, **kwds: Any):
        if self.daily_schedule.is_day_off:
            raise validators.ValidationError('Breaks cannot be set to dat off.')
            
        self.bulk_create()
        
    def validate_breaks_intersection(self, breaks):
        current_breaks = self.daily_schedule.breaks.all()
        breaks += list(current_breaks)
        intervals = [Interval(b.start_break_time_step, b.end_break_time_step) for b in breaks]
        
        if is_intersect(intervals, len(intervals)):
            raise serializers.ValidationError('Break time intervals cannot intersect between each other.')
        
        work_day_interval = Interval(self.daily_schedule.start_work_time_step, self.daily_schedule.end_work_time_step)
        if not is_intersect_with(work_day_interval, intervals):
            raise serializers.ValidationError('Work day interval must include all breaks intervals.')  
    
    def validate_break(self, daily_break: StaffBreak):
        if not daily_break.start_break_time_step or not daily_break.end_break_time_step:
            raise serializers.ValidationError('Time step cannot be empty.')
        
        if daily_break.end_break_time_step - daily_break.start_break_time_step <= 0:
            raise validators.ValidationError('End break time step must be greater than start time step.')
    
    def bulk_create(self) -> StaffBreak:
        def _get_breaks():
            for day_break in self.breaks:
                staff_break = StaffBreak(
                    start_break_time_step = day_break.get('start_break_time_step'),
                    end_break_time_step = day_break.get('end_break_time_step'),
                    schedule=self.daily_schedule
                )
                self.validate_break(staff_break)
                yield staff_break
                
        breaks = [b for b in _get_breaks()]
        self.validate_breaks_intersection(breaks)
        
        StaffBreak.objects.bulk_create(breaks)