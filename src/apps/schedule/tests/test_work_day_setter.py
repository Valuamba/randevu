import pytest
from apps.schedule.services import WorkDaySetter

from randevu import validators
from apps.schedule.services.day_off_setter import DayOffScheduleSetter

from django.conf import settings


pytestmark = [pytest.mark.django_db]



@pytest.fixture
def setter():
    return lambda *args, **kwargs: WorkDaySetter(*args, **kwargs)


@pytest.fixture(autouse=True)
def breaks_creator(mocker):
    return mocker.patch('apps.schedule.services.DailyBreaksCreator.__call__')


@pytest.fixture
def work_day(mixer):
   return mixer.blend('schedule.StaffSchedule', is_day_off=False, start_work_time_step=36,
                       end_work_time_step=70)


@pytest.fixture
def zero_breaks_work_day(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=False, start_work_time_step=36,
                       end_work_time_step=70)
    
    
@pytest.fixture
def day_off(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=True, start_work_time_step=36,
                       end_work_time_step=70)
    
@pytest.fixture
def update_data():
    return {
        'start_work_time_step': 36,
        'end_work_time_step': 70
    }
    
def test_work_day_setter(setter, day_off):
    setter(day_off, {
        'start_work_time_step': 36,
        'end_work_time_step': 70
    })()
    
    day_off.refresh_from_db()
    
    assert day_off.is_day_off == False
    assert day_off.start_work_time_step == 36
    assert day_off.end_work_time_step == 70
    assert day_off.breaks.all().count() == 0
    
    
def test_work_day_setter_breaks(mixer, setter, day_off, breaks_creator, update_data):
    breaks = [mixer.blend('schedule.StaffBreak').__dict__ for i in range(3)]

    setter(day_off, {
        **update_data,
        'breaks': breaks
    })()
    
    day_off.refresh_from_db()
    
    breaks_creator.assert_called_once()
    assert day_off.breaks.all().count() == 0
    

def test_setter_for_work_day(setter, work_day, update_data):
    with pytest.raises(validators.ValidationError) as err:
        setter(work_day, update_data)()
        
        assert 'You cannot say already work day to work day.' in err.get('detail').lower()
        
        
@pytest.mark.parametrize(
    ('start', 'end'),
    [
        (None, None),
        (0, 0),
        (20, 10),
        (30, 400),
    ]
)
def test_not_valid_updated_data(setter, day_off, start, end):
     with pytest.raises(validators.ValidationError) as err:
        setter(day_off, {
            'start_work_time_step': start,
            'end_work_time_step': end,
        })()
                