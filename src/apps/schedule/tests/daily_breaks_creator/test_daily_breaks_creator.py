import pytest

from randevu import validators

pytestmark = [pytest.mark.django_db]


def test_breaks_creating(create, work_day):
    create(work_day, breaks=[
        {
            'start_break_time_step': 50,
            'end_break_time_step': 70
        }
    ])
    
    work_day.refresh_from_db()
    breaks = work_day.breaks.all()
    
    assert len(breaks) == 1
    assert breaks[0].start_break_time_step == 50
    assert breaks[0].end_break_time_step ==  70
    
    
def test_multiple_breaks(create, work_day):
    create(work_day, breaks=[
        {
            'start_break_time_step': 50,
            'end_break_time_step': 70
        },
        {
            'start_break_time_step': 74,
            'end_break_time_step': 85
        }
    ])
    
    work_day.refresh_from_db()
    breaks = work_day.breaks.all()
    
    assert len(breaks) == 2
    assert breaks[0].start_break_time_step == 50
    assert breaks[0].end_break_time_step == 70
    assert breaks[1].start_break_time_step == 74
    assert breaks[1].end_break_time_step ==  85
    
    
def test_start_step_less_than_end(create, work_day):
    with pytest.raises(validators.ValidationError) as err:
        create(work_day, breaks=[
            {
                'start_break_time_step': 70,
                'end_break_time_step': 50
            }
        ])
        
        assert 'End break time step must be greater than start time step.' in str(err['detail']).lower()
