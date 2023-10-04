import pytest

from typing import Dict, Any
from django.utils import timezone
from django.conf import settings

from apps.schedule.models import StaffBreak, StaffSchedule


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time('2022-11-16 15:30:45'), 
]

NOVEMBER_MONDAY = 21
NOVEMBER_SUNDAY = 20


# @pytest.fixture(autouse=True)
# def _set_time_step_range():
#     settings.TIME_STEP_MINUTES = 15


@pytest.fixture
def service(mixer, employee):
    return mixer.blend('service.SalonService', company=employee.company, duration=2)


@pytest.fixture
def employee(factory):
    return factory.employee(name='Авраам Соломонович Пейзенгольц', email='abraham@gmail.com')


@pytest.fixture
def work_monday(factory, employee):
    return factory.daily_schedule(week_day=StaffSchedule.MONDAY, is_day_off=False, user=employee,
                            start_work_time_step=0, end_work_time_step=16,
                            breaks=[
                                StaffBreak(start_break_time_step=2, end_break_time_step=4),
                                StaffBreak(start_break_time_step=8, end_break_time_step=9),
                                StaffBreak(start_break_time_step=12, end_break_time_step=13),
                            ])


@pytest.fixture(autouse=True)
def init_week_schedule(factory, employee):
    for day in StaffSchedule.DAYS_OF_WEEK_ARR[1:]:
        factory.daily_schedule(week_day=day, is_day_off=True, user=employee)


@pytest.fixture
def payload(employee, service):
    return {
        'service_id': service.pkid,
        'employee_id': employee.pkid,
        'month': timezone.now().date().month,
        'year': timezone.now().date().year
    }


def test_work_slots_default_employee(anon, payload, employee, work_monday):
    result = anon.post('/api/v2/employee/times/', payload, expected_status_code=200, 
     **{ 'HTTP_SFC_DNS_ZONE': employee.company.sub_domain }
    )

    days: Dict[int, Any] = result['days']

    assert len(days) == 30
    assert days[str(NOVEMBER_MONDAY)]['status'] == True

    # print(days)
    assert [slot['value'] for slot in days[str(NOVEMBER_MONDAY)]['free_time_slots']] == [0, 4, 5, 6, 9, 10, 13, 14]


def test_work_slots_default_employee_1(anon, payload, employee, work_monday):
    result = anon.post('/api/v2/employee/times/', payload, expected_status_code=200,
        **{ 'HTTP_SFC_DNS_ZONE': employee.company.sub_domain }
    )

    days: Dict[int, Any] = result['days']

    assert len(days) == 30
    assert days[str(NOVEMBER_SUNDAY)]['status'] == False
    assert days[str(NOVEMBER_SUNDAY)]['free_time_slots'] == []