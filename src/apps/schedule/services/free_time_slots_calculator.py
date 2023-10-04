from typing import Any

from apps.users.models import User


class FreeTimeSlotsCalculator:
    def __init__(self, employee: User) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        employee = self.employee

        employee.weekly_schedule

        employee.appointments
