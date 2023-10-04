import pytest

from apps.users.models import User
from apps.schedule.models import StaffSchedule, StaffBreak
from apps.employee.services import EmployeeMonthTimeSlots

from django.utils import timezone

pytestmark = [ 
    pytest.mark.django_db,
    pytest.mark.freeze_time('2022-11-16 15:30:45'), 
]


def test_appointment(user: User, appointment, work_monday):
    appointments = user.get_employee_appointments_by_month(2022, 11)

    assert len(appointments) == 1
    assert appointments[appointment.day.day] == {4, 5}


def test_month_day_ranges(user: User, appointment, work_monday, service):
    days_range = EmployeeMonthTimeSlots(user, 2022, 11, service)()

    assert [ slot['value'] for slot in days_range['days'][appointment.day.day]['free_time_slots']] == [0, 6, 9, 10, 13, 14]


def test_day_off(user: User, appointment, work_monday, service):
    days_range = EmployeeMonthTimeSlots(user, 2022, 11, service)()

    assert days_range['days'][16]['status'] == False
    assert days_range['days'][17]['status'] == False
