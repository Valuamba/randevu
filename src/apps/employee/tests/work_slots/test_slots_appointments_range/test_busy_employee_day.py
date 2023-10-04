import pytest

from apps.users.models import User
from apps.employee.services import EmployeeMonthTimeSlots
from apps.schedule.models import StaffSchedule, StaffBreak

from django.utils import timezone
import datetime


pytestmark = [ 
    pytest.mark.django_db,
    pytest.mark.freeze_time('2022-11-16 15:30:45'), 
]


@pytest.fixture
def one_time_service(mixer):
    return mixer.blend('service.SalonService', pkid=3, duration=2)


@pytest.fixture
def two_time_service(mixer):
    return mixer.blend('service.SalonService', pkid=3, duration=2)


@pytest.fixture
def appointment(mixer, user, one_time_service, two_time_service, category):
    def _create_appointment(time_step: int, service):
        mixer.blend('appointment.Appointment', employee=user, day=datetime.datetime(2022, 11, 21),
            service=service, category=category, time_step=time_step
        )
    _create_appointment(0, two_time_service)
    _create_appointment(4, one_time_service)
    _create_appointment(5, one_time_service)
    _create_appointment(6, two_time_service)
    _create_appointment(9, two_time_service)
    _create_appointment(11, one_time_service)
    _create_appointment(13, one_time_service)
    _create_appointment(14, two_time_service)


@pytest.fixture
def work_monday(factory, user):
    return factory.daily_schedule(week_day=StaffSchedule.MONDAY, is_day_off=False, user=user,
                            start_work_time_step=0, end_work_time_step=16,
                            breaks=[
                                StaffBreak(start_break_time_step=2, end_break_time_step=4),
                                StaffBreak(start_break_time_step=8, end_break_time_step=9),
                                StaffBreak(start_break_time_step=12, end_break_time_step=13),
                            ])


@pytest.fixture(autouse=True)
def init_week_schedule(factory, user):
    for day in StaffSchedule.DAYS_OF_WEEK_ARR[1:]:
        factory.daily_schedule(week_day=day, is_day_off=True, user=user)


def test_appointment(user: User, appointment, work_monday):
    appointments = user.get_employee_appointments_by_month(2022, 11)

    assert len(appointments) == 1
    assert appointments[21] == { 0, 1, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15 }


def test_month_day_ranges(user: User, appointment, work_monday, service):
    days_range = EmployeeMonthTimeSlots(user, 2022, 11, service)()

    assert days_range['days'][21]['status'] == False