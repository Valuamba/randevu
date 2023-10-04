import pytest 

from apps.employee.services import EmployeeMonthTimeSlots


pytestmark = [
    pytest.mark.django_db
]


def test_free_duration_slots():
    duration = 2

    range_without_duration = [1, 2, 4, 5, 6, 8, 9, 10, 11, 15]
    work_slots = EmployeeMonthTimeSlots.get_free_slots_meets_duration(range_without_duration, duration)

    assert work_slots == [1, 4, 5, 8, 9, 10]


@pytest.mark.parametrize('duration', [0, 1])
def test_free_slots_without_duration(duration):
    range_without_duration = [1, 2, 4, 5, 6, 8, 9, 10, 11, 15]
    work_slots = EmployeeMonthTimeSlots.get_free_slots_meets_duration(range_without_duration, duration)

    assert work_slots == [1, 2, 4, 5, 6, 8, 9, 10, 11, 15]