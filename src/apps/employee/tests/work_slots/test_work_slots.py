import pytest

from apps.users.models import User
from apps.schedule.models import StaffSchedule, StaffBreak


pytestmark = [ 
    pytest.mark.django_db,
    pytest.mark.freeze_time('2022-11-16 15:30:45'), 
]


@pytest.fixture
def work_monday(factory, user):
    return factory.daily_schedule(week_day=StaffSchedule.MONDAY, is_day_off=False, user=user,
                            start_work_time_step=0, end_work_time_step=16,
                            breaks=[
                                StaffBreak(start_break_time_step=2, end_break_time_step=4),
                                StaffBreak(start_break_time_step=8, end_break_time_step=9),
                                StaffBreak(start_break_time_step=12, end_break_time_step=13),
                            ])

 
@pytest.fixture
def day_off_sunday(factory, user):
    return factory.daily_schedule(week_day=StaffSchedule.SUNDAY, is_day_off=True, user=user)


def test_weekly_free_slots(user: User, work_monday):
    ''' Work shift: 00:00-08:00 
        breaks: 01:00-02:00, 04:00-04:30, 06:00-06:30 
    '''
    slots = user.get_work_slots()

    assert work_monday.week_day in slots.keys()
    assert slots[work_monday.week_day] == {0, 1, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15}


def test_slot_off_day(user: User, day_off_sunday: StaffSchedule):
    slots = user.get_work_slots()

    assert day_off_sunday.week_day in slots.keys()
    assert slots[day_off_sunday.week_day] == None

# def test_available_employee_days(user: User):
#     days = user.get_employee_work_days(2022, 11)
    
#     assert days == [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
