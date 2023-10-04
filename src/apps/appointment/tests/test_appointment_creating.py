import datetime
import pytest

from freezegun.api import FakeDatetime, datetime_to_fakedatetime 

from django.utils import timezone
import zoneinfo
from dateutil import tz
# from freezegun.api. 

pytestmark = [ 
    pytest.mark.django_db,
    pytest.mark.single_thread,
    # pytest.mark.freeze_time('2022-11-16 00:10:45')
]

from apps.appointment.models import Appointment


@pytest.fixture(autouse=True)
def _set_timezone(settings):
    settings.USE_TZ = True
    settings.TIME_ZONE = 'Europe/Moscow'


@pytest.fixture
def payload(service, category, employee):
    return {
        'employee': employee.pkid,
        'category': category.pkid,
        'service': service.pkid,
        'client': {
            'name': 'Петрo',
            'phone': '+375298914939'
        },
        'time_step': 2,
        'day': '2022-11-18'
    }

# def test_appointment_timezone(anon, payload, service, category, employee):
#     anon.post('/api/v2/appointment/', payload, expected_status_code=200)

#     result = Appointment.objects.order_by('-id').first()

#     assert result.employee == employee
#     assert result.category == category
#     assert result.service == service
#     assert result.day == datetime.date(2022, 11, 18)