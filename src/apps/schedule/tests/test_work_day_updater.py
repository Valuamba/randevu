import pytest
from apps.schedule.services import WorkDayUpdater

from randevu import validators

pytestmark = [pytest.mark.django_db]



@pytest.fixture(autouse=True)
def reset_breaks(mocker):
    return mocker.patch('apps.schedule.models.StaffSchedule.reset_breaks')


@pytest.fixture(autouse=True)
def breaks_creator(mocker):
    return mocker.patch('apps.schedule.services.DailyBreaksCreator.__call__')


@pytest.fixture
def setter():
    return lambda *args, **kwargs: WorkDayUpdater(*args, **kwargs)


@pytest.fixture
def update_data():
    return {
        'start_work_time_step': 36,
        'end_work_time_step': 70
    }
    

def test_update_dayoff(setter, day_off, update_data):
    with pytest.raises(validators.ValidationError):
        setter(day_off, update_data)()
        

@pytest.mark.parametrize(
    ('start', 'end'),
    [
        (None, None),
        (0, 0),
        (20, 10),
        (30, 400),
    ]
)
def test_not_valid_updated_data(setter, work_day, start, end):
     with pytest.raises(validators.ValidationError) as err:
        setter(work_day, {
            'start_work_time_step': start,
            'end_work_time_step': end,
        })()
        
        
def test_update_work_day(setter, work_day):
    setter(work_day, {
        'start_work_time_step': 33,
        'end_work_time_step': 89
    })()
    
    work_day.refresh_from_db()
    
    assert work_day.start_work_time_step == 33
    assert work_day.end_work_time_step == 89
    assert work_day.breaks.all().count() == 0
    
    
def test_update_work_day_breaks(mixer, setter, work_day, update_data, reset_breaks, breaks_creator):
    setter(work_day, {
        **update_data,
        'breaks': [mixer.blend('schedule.StaffSchedule').__dict__ for i in range(3)]
    })()
    
    reset_breaks.assert_called_once()
    breaks_creator.assert_called_once()
      