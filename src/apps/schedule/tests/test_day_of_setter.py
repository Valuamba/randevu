import pytest

from randevu import validators
from apps.schedule.services.day_off_setter import DayOffScheduleSetter

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def setter():
    return lambda *args, **kwargs: DayOffScheduleSetter(*args, **kwargs)


@pytest.fixture
def work_day(mixer):
    staff =  mixer.blend('schedule.StaffSchedule', is_day_off=False, start_work_time_step=36,
                       end_work_time_step=70)
    
    breaks = [mixer.blend('schedule.StaffBreak') for i in range(3)]
        
    staff.breaks.set(breaks)
    return staff


@pytest.fixture
def zero_breaks_work_day(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=False, start_work_time_step=36,
                       end_work_time_step=70)
    
    
@pytest.fixture
def day_off(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=True, start_work_time_step=36,
                       end_work_time_step=70)
    
    
                           
def test_set_work_day_with_dayoff(setter, work_day):
    setter(work_day)()
    
    work_day.refresh_from_db()
    
    assert work_day.is_day_off == True
    assert work_day.start_work_time_step == None
    assert work_day.end_work_time_step == None
    assert work_day.breaks.all().count() == 0
    
    
def test_set_with_zero_breaks(setter, zero_breaks_work_day):
    setter(zero_breaks_work_day)()
    
    zero_breaks_work_day.refresh_from_db()
    
    assert zero_breaks_work_day.is_day_off == True
    assert zero_breaks_work_day.start_work_time_step == None
    assert zero_breaks_work_day.end_work_time_step == None
    assert zero_breaks_work_day.breaks.all().count() == 0
    
    
def test_setter_for_dayoff(setter, day_off):
    with pytest.raises(validators.ValidationError) as err:
        setter(day_off)()
    
        assert 'Day is already day off.' in err.get('detail').lower()