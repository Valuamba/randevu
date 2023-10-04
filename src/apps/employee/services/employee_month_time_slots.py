from typing import  Any, Dict, List

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from apps.service.models import SalonService
from apps.utils import present_time_slots_with_label

import datetime
from dateutil import tz
import calendar


#ToDO: не забыть про временную зону для каждой из стран
class EmployeeMonthTimeSlots:
    def __init__(self, user: User, year: int, month: int, service: SalonService = None) -> None:
        self.user = user
        self.year = year
        self.month = month
        self.service = service

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.get_employee_work_days(self.user, self.year, self.month, self.service)

    def get_employee_work_days(self, user: User, year: int, month: int, service: SalonService) -> Any:
        day_infos: Dict[int, dict] = {}

        duration = service.duration if service else 1
        print(f'DUR: {duration}')
        work_slots = user.get_work_slots(duration)
        appointments = user.get_employee_appointments_by_month(year, month)

        current_date = timezone.now().date()
        for day in self.manage_day_range(year, month):

            day_data = datetime.datetime(year, month, day)
            week_day = day_data.weekday()
            work_range = work_slots.get(week_day, None)

            'Check that day is not outdated and that day is not day off'
            if current_date <= day_data.date() and work_range:
                appointment_range = appointments.get(day, set())
                work_free_slots = list(work_range - appointment_range)
                work_free_slots = self.get_free_slots_meets_duration(work_free_slots, duration)

                day_infos[day] = { 
                    'status': len(work_free_slots) > 0,
                    'free_time_slots': present_time_slots_with_label(work_free_slots)
                }
            else:
                day_infos[day] = { 
                    'status': False,
                    'free_time_slots': []
                }

        return {
            'days': day_infos
        }

    @staticmethod
    def get_free_slots_meets_duration(work_time_range: List[int], duration = 0):
        '''This method calculates time slots that meet duration condition
           For example: duration = 2, slots = [11, 12, 14, 16, 17, 18] then valid slots
           to create appointment [11, 16, 17]
        '''

        if duration > 1:
            count = len(work_time_range)
            new_work_range = []
            for i in range(count):
                counter = 0

                if count < i + duration:
                    continue

                for j in range(i, i + duration - 1):
                    if work_time_range[j + 1] - work_time_range[j] == 1:
                        counter += 1
                    else:
                        break

                if counter >= duration - 1:
                    new_work_range.append(work_time_range[i])

            return new_work_range
        else:
            return work_time_range

    @staticmethod
    def manage_day_range(year: int, month: int):
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            for day in week:
                if day != 0:
                    yield day