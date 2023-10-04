import datetime
import pytest

from django.utils import timezone

from freezegun.api import FakeDatetime, datetime_to_fakedatetime
from dateutil import tz
import zoneinfo
# from freezegun.api. 

from apps.appointment.models import Appointment


pytestmark = [ 
    pytest.mark.django_db,
    pytest.mark.single_thread,
    pytest.mark.freeze_time('2022-11-16 00:10:45')
]


@pytest.fixture(autouse=True)
def _set_timezone(settings):
    settings.USE_TZ = True
    settings.TIME_ZONE = 'UTC'


def test_timezone_now():

   
    timezone.activate(zoneinfo.ZoneInfo('Europe/Moscow'))

    fake_date_time = datetime_to_fakedatetime(
        datetime.datetime(2022, 11, 16, 00, 10, 45, tzinfo=tz.gettz('UTC'))
    )
    assert timezone.now() == fake_date_time