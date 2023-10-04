import pytest
from apps.schedule.services import WeeklyScheduleCreator

from randevu import validators

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def creator():
    return lambda *args, **kwargs: WeeklyScheduleCreator(*args, **kwargs)


def test_weekly_creator(creator, user):
    creator(user)()
    
    user.refresh_from_db()
    
    assert user.weekly_schedule.all().count() == 7
    
    
def test_weekly_creator_with_added_schedule(creator, user, mixer):
    user.weekly_schedule.set([ mixer.blend('schedule.StaffSchedule', week_day=i) for i in range(3)])
    
    with pytest.raises(validators.ValidationError) as err:
        creator(user)()

    