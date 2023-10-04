import pytest

from apps.users.models import User
from apps.schedule.models import StaffSchedule, StaffBreak

from django.utils import timezone
import datetime

@pytest.fixture
def employee(mixer):
    return mixer.blend('users.User', pkid=2, name='Авраам Соломонович Пейзенгольц', email='abraham@gmail.com')


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService', pkid=3, duration=2)


@pytest.fixture
def category(mixer):
    return mixer.blend('service.Category', pkid=1)


@pytest.fixture
def appointment(mixer, user, service, category):
    return mixer.blend('appointment.Appointment', employee=user, day=datetime.datetime(2022, 11, 21),
        service=service, category=category, time_step=4
    )


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
