from rest_framework import serializers

from dataclasses import dataclass
from typing import Any, List

from django.conf import settings
from django.db.transaction import atomic

from apps.schedule.models import StaffSchedule, StaffBreak
from apps.users.models import User


# TODO: add multilanding schedule validation
# add booked time by appointment and breaks on this time validation


DAYS_OF_WEEK = [
        StaffSchedule.MONDAY, StaffSchedule.TUESDAY, 
        StaffSchedule.WEDNESDAY, StaffSchedule.THURSDAY,
        StaffSchedule.FRIDAY, StaffSchedule.SUNDAY, StaffSchedule.SATURDAY
    ]


class StaffScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSchedule
        fields = [
            'week_day',
            'start_work_time_step',
            'end_work_time_step',
            'is_day_off',
            'user'
        ]


@dataclass
class StaffScheduleCreator:
    user: User
    schedule: List[StaffSchedule]
    
    @atomic
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.create_staff_schedule()
        
    def create_weekly_schedule(self):
        added_days_of_week = []

        for daily_schedule in self.schedule:
            breaks = daily_schedule.pop('breaks')
            
            serializer = StaffScheduleCreateSerializer(data={
                **daily_schedule,
                'user': self.user_id
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            schedule_id = serializer.data.get('pkid')

            self.create_breaks(breaks, schedule_id)
            
            added_days_of_week.append(daily_schedule.get('week_day'))  
            
        self.create_off_days(added_days_of_week)
        
    # def create_day_of_week_schedule(self, ):
    #     StaffSchedule.objects.create(
    #         week_day=
    #     )
 
        
    # def create    

    def create_breaks(self, breaks: List[StaffBreak], schedule_id: int):
        if len(breaks) > settings.MAX_STAFF_BREAKS_COUNT:
                raise Exception(f'There are exceed max amount of breaks - {settings.MAX_STAFF_BREAKS_COUNT}')
            
        bulk_breaks = []
        for daily_break in bulk_breaks:
            bulk_breaks.append(StaffBreak(
                start_break_time_step=daily_break.get('start_break_time_step'),
                steps_amount=daily_break.get('steps_amount'),
                schedule_id=schedule_id
            ))
                
        StaffBreak.objects.bulk_create(bulk_breaks)
        
    def create_off_days(self, added_days_of_week: List[int]):
        days_without_schedule = list(set(self.DAYS_OF_WEEK).symmetric_difference(set(added_days_of_week)))        
        
        off_days = []
        for day in days_without_schedule:
            off_days.append(StaffSchedule(
                week_day = day,
                user_id = self.user_id,
                start_work_time_step = None,
                end_work_time_step = None,
                is_day_off = True,
            ))
            
        StaffSchedule.objects.bulk_create(off_days)
    