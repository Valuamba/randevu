from typing import List, Any

from apps.schedule.models import StaffSchedule
from apps.users.models import User

from randevu import validators

DAYS_OF_WEEK = [
        StaffSchedule.MONDAY, StaffSchedule.TUESDAY, 
        StaffSchedule.WEDNESDAY, StaffSchedule.THURSDAY,
        StaffSchedule.FRIDAY, StaffSchedule.SUNDAY, StaffSchedule.SATURDAY
]


class WeeklyScheduleCreator:
    def __init__(self, user: User) -> None:
        self.user = user
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.user.weekly_schedule and self.user.weekly_schedule.all().count() > 0:
            raise validators.ValidationError('User already has weekyly schedule.')
        
        self.create()
    
    def create(self) -> List[StaffSchedule]:
        days = []
        for day in DAYS_OF_WEEK:
            days.append(StaffSchedule(
                week_day = day,
                start_work_time_step = None,
                end_work_time_step = None,
                is_day_off = True,
                user=self.user
            ))
            
        StaffSchedule.objects.bulk_create(days)

        return days