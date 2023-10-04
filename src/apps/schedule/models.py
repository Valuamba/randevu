from asyncio import constants
from typing import List
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models import QuerySet

from apps.common.models import TimeStampedUUIDModel


class StaffSchedule(TimeStampedUUIDModel):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    DAYS_OF_WEEK = [
        (MONDAY, _("Monday")),
        (TUESDAY, _("Tuesday")),
        (WEDNESDAY, _("Wednesday")),
        (THURSDAY, _("Thursday")),
        (FRIDAY, _("Friday")),
        (SUNDAY, _("Sunday")),
        (SATURDAY, _("Saturday"))
    ]
    
    DAYS_OF_WEEK_ARR = [ MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY ]

    week_day = models.IntegerField(verbose_name=_("Week day"), choices=DAYS_OF_WEEK, null=False)
    start_work_time_step = models.IntegerField(verbose_name=_("Start work time step"), null=True)
    end_work_time_step = models.IntegerField(verbose_name=_("End work time step"), null=True)
    
    is_day_off = models.BooleanField(verbose_name=_("Is day OFF"), default=True)
    
    user = models.ForeignKey('users.User', related_name='weekly_schedule', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "staff.schedule"
        verbose_name = _('Staff schedule')
        verbose_name_plural = _('Staffs schedule')

        constraints = [
            models.UniqueConstraint(fields=['week_day', 'user'], name='single schedule for one week day'),
        ]

    def get_work_time_range(self, duration = 0) -> set:
        work_time_range = set(range(self.start_work_time_step, self.end_work_time_step))
        for break_range in self.breaks.all():
            work_time_range -= break_range.get_break_range() 
        return work_time_range

    def update_work_time(self, day_data: dict):
        from apps.schedule.services import WorkDayUpdater
        WorkDayUpdater(self, day_data)()
        
    def mark_as_day_off(self):
        from apps.schedule.services import DayOffScheduleSetter
        DayOffScheduleSetter(self)()
        
    def mark_as_work_day(self, work_day_data: dict):
        from apps.schedule.services import WorkDaySetter
        WorkDaySetter(self, work_day_data)()
    
    def reset_breaks(self):
        def _get_breaks() -> QuerySet[StaffBreak]:
            return self.breaks
        _get_breaks().all().delete()    
        
    def set_breaks(self, breaks: List[dict]):
        from apps.schedule.services import DailyBreaksCreator
        DailyBreaksCreator(self, breaks)()
    
        

class StaffBreak(TimeStampedUUIDModel):
    start_break_time_step = models.IntegerField(verbose_name=_("Start break time step"), null=False)
    end_break_time_step = models.IntegerField(verbose_name=_("Steps amount"), null=False)
    
    schedule = models.ForeignKey(StaffSchedule, related_name="breaks", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "staff.break"
        verbose_name = _('Staff break')
        verbose_name_plural = _('Staff breaks')
        
        constraints = [
            models.UniqueConstraint(fields=['start_break_time_step', 'schedule'], name='Single break time step')
        ]
        
    def get_break_range(self) -> set:
        return set(range(self.start_break_time_step, self.end_break_time_step))