import pytest
from randevu import validators 

pytestmark = [pytest.mark.django_db]
        

@pytest.fixture
def interval_work_day(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=False, start_work_time_step=36,
                       end_work_time_step=60, week_day=3)
    

@pytest.mark.parametrize(
    ('start_step', 'end_step'), 
    [
        (35, 38), (35, 41), (38, 39), (39, 45), (37, 40), (37, 41), (40, 46), (35, 37)
    ]
)
def test_two_intersect_in_breaks(create, work_day, start_step, end_step):
    with pytest.raises(validators.ValidationError) as err:
        create(work_day, breaks=[
            {
                    'start_break_time_step': 37,
                    'end_break_time_step': 40
            },
            {
                    'start_break_time_step': start_step,
                    'end_break_time_step': end_step
            }
        ])
                
        assert 'intersect' in str(err['detail']).lower()
    
    
def test_multiple_intersects(create, work_day):
    with pytest.raises(validators.ValidationError) as err:
        create(work_day, breaks=[
            {
                    'start_break_time_step': 37,
                    'end_break_time_step': 40
            },
            {
                    'start_break_time_step': 35,
                    'end_break_time_step': 38
            },
            {
                    'start_break_time_step': 45,
                    'end_break_time_step': 50
            }
        ])
                
        assert 'intersect' in str(err['detail']).lower()
        
#36-60
@pytest.mark.parametrize(
    ('start_step', 'end_step'), 
    [
        (20, 30), (20, 41), (20, 36), (36, 70), (40, 70), (60, 70), (20, 60), (70, 80)
    ]
)     
def test_out_of_work_day_interval(create, interval_work_day, start_step, end_step):
    with pytest.raises(validators.ValidationError) as err:
        create(interval_work_day, breaks=[
            {
                    'start_break_time_step': start_step,
                    'end_break_time_step': end_step
            },
        ])
                
        assert 'Work day interval must include all breaks intervals.' in str(err['detail']).lower()
        
        
@pytest.mark.parametrize(
    ('start_step', 'end_step'), 
    [
        (36, 39), (36, 60), (40, 60), (50, 60)
    ]
)        
def test_include_breaks_in_work_day_interval(create, interval_work_day, start_step, end_step):
    create(interval_work_day, breaks=[
            {
                    'start_break_time_step': start_step,
                    'end_break_time_step': end_step
            },
        ])
                
    interval_work_day.refresh_from_db()   
    breaks = list(interval_work_day.breaks.all())
    
    assert breaks[0].start_break_time_step == start_step
    assert breaks[0].end_break_time_step == end_step
    