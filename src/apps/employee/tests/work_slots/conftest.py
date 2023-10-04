
from rest_framework.test import APIClient
from mixer.backend.django import mixer
import pytest
from django.conf import settings
from unittest.mock import MagicMock
from mixer.backend.django import mixer as _mixer


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def user(mixer):
    return mixer.blend('users.User', pkid=1)


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def connect_mock_handler():
    def _connect_mock_handler(signal, **kwargs):
        handler = MagicMock()
        signal.connect(handler, **kwargs)
        return handler
    
    return _connect_mock_handler


@pytest.fixture
def domain(mixer):
    return mixer.blend('multilanding.MultilandingDomain', domain=settings.RANDEVU_DOMAIN)


'''
00:00 - 0
00:30 - 1
01:00 - 2
01:30 - 3
02:00 - 4
02:30 - 5
03:00 - 6
03:30 - 7
04:00 - 8
04:30 - 9
05:00 - 10
05:30 - 11
06:00 - 12
06:30 - 13
07:00 - 14
07:30 - 15
08:00 - 16
08:30 - 17
09:00 - 18
09:30 - 19
10:00 - 20
10:30 - 21
11:00 - 22
11:30 - 23
12:00 - 24
12:30 - 25
13:00 - 26
13:30 - 27
14:00 - 28
14:30 - 29
15:00 - 30
'''

def build_breaks(mixer, breaks):
    breaks_mixer = [] 
    for b in breaks:
        mock_break = mixer.blend('schedule.StaffBreak', 
            start_break_time_step=b['start_break_time_step'],
            end_break_time_step=b['end_break_time_step']
        )
        breaks_mixer.append(mock_break)
    return breaks_mixer
    

def build_weekly_schedule(mixer, user, weekly_schedule):
    mock_days = []
    for day in weekly_schedule:
        staff_schedule = mixer.blend('schedule.StaffSchedule', 
            week_day=day['week_day'],
            is_day_off=day['is_day_off'], 
            start_work_time_step=day['start_work_time_step'],
            end_work_time_step=day['end_work_time_step'])
        
        staff_schedule.breaks.set(build_breaks(mixer, day['breaks']))
        mock_days.append(staff_schedule)
    
    user.weekly_schedule.set(mock_days)
    return user  


#  {
#             'week_day': StaffSchedule.MONDAY,
#             'is_day_off': False,
#             'start_work_time_step': 0,
#             'end_work_time_step': 16,
#             'breaks': [
#                 {
#                     'start_break_time_step': 2,
#                     'end_break_time_step': 4
#                 },
#                 {
#                     'start_break_time_step': 8,
#                     'end_break_time_step': 9
#                 },
#                 {
#                     'start_break_time_step': 12,
#                     'end_break_time_step': 13
#                 }
#             ]
#         }
#     ]

# @pytest.fixture
# def build_week(factory, user):
#     factory.daily_schedule(week_day= user=user, breaks)
