import pytest
from apps.schedule.models import StaffSchedule
from apps.schedule.services import WeeklyScheduleUpdater

from randevu import validators

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def updater():
    return lambda *args, **kwargs: WeeklyScheduleUpdater(*args, **kwargs)


@pytest.fixture(autouse=True)
def breaks_creator(mocker):
    return mocker.patch('apps.schedule.services.DailyBreaksCreator.__call__')


@pytest.fixture(autouse=True)
def work_day_setter(mocker):
    return mocker.patch('apps.schedule.services.WorkDaySetter.__call__')


@pytest.fixture(autouse=True)
def work_day_updater(mocker):
    return mocker.patch('apps.schedule.services.WorkDayUpdater.__call__')


@pytest.fixture(autouse=True)
def day_off_setter(mocker):
    return mocker.patch('apps.schedule.services.DayOffScheduleSetter.__call__')


@pytest.fixture
def schedule_user(mixer):
    user = mixer.blend('users.User')
        
    user.weekly_schedule.set([
        mixer.blend('schedule.StaffSchedule', week_day=0, is_day_off=True),
        mixer.blend('schedule.StaffSchedule', week_day=1, is_day_off=False, start_work_time_step=40, end_work_time_step=80),
    ])
    
    return user

def test_weekly_work_day_setter(updater, schedule_user, work_day_setter, work_day_updater, day_off_setter):
    updater(schedule_user, [
        {
        'week_day': 0,
        'is_day_off': False,
        'start_work_time_step': 50,
        'end_work_time_step': 60
        }
    ])()
    
    work_day_setter.assert_called_once()
    work_day_updater.assert_not_called()
    day_off_setter.assert_not_called()
    
    
def test_weekly_work_day_updater(updater, schedule_user, work_day_updater, work_day_setter, day_off_setter):
    updater(schedule_user, [
        {
            'week_day': 1,
            'start_work_time_step': 50,
            'end_work_time_step': 60
        }
    ])()
    
    work_day_updater.assert_called_once()
    day_off_setter.assert_not_called()
    work_day_setter.assert_not_called()


def test_weekly_day_off_setter(updater, schedule_user, day_off_setter, work_day_updater, work_day_setter):
    updater(schedule_user, [
        {
            'week_day': 1,
            'is_day_off': True,
            'start_work_time_step': 50,
            'end_work_time_step': 60
        }
    ])()
    
    day_off_setter.assert_called_once()
    work_day_updater.assert_not_called()
    work_day_setter.assert_not_called()