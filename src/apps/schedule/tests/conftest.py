from apps.schedule.models import StaffSchedule
import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def _set_time_step_range(settings):
    settings.TIME_STEP_MINUTES = 15
    settings.MAX_TIME_STEPS = int(24 * 60 / settings.TIME_STEP_MINUTES) 


@pytest.fixture
def work_day(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=False, start_work_time_step=36,
                       end_work_time_step=90, week_day=StaffSchedule.MONDAY)
    
    
@pytest.fixture
def day_off(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=True,
                       start_work_time_step=36,
                       end_work_time_step=90, week_day=StaffSchedule.MONDAY)


@pytest.fixture
def user(mixer):
    return mixer.blend('users.User')