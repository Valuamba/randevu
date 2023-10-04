from apps.schedule.models import StaffBreak, StaffSchedule
from apps.users.models import User

from typing import List
from randevu.test.factory import register


@register
def daily_schedule(self, user: User, breaks: List[StaffBreak] = [], **kwargs):
    schedule = self.mixer.blend('schedule.StaffSchedule', user=user, **kwargs)

    if len(breaks) > 0:
        schedule.breaks.set(breaks, bulk=False)
        schedule.save()

    return schedule