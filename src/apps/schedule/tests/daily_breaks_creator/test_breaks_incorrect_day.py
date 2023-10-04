import pytest
from randevu import validators 

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def day_off(mixer):
    return mixer.blend('schedule.StaffSchedule', is_day_off=True)
    
    
def test_breaks_creating(create, day_off):
    with pytest.raises(validators.ValidationError) as err:
        create(day_off, breaks=[])
        
        assert 'Breaks cannot be set to dat off.' in err['detail']
        