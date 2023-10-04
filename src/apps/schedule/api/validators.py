from django.forms import ValidationError
from randevu import validators
from typing import Any

from django.conf import settings


class StaffBreakValidator(validators.Validator):
    start_break_time_step = validators.IntegerField(required=True)
    end_break_time_step = validators.IntegerField(required=False)
    
    
class ScheduleValidator(validators.Validator):
    week_day = validators.IntegerField(required=True)
    start_work_time_step = validators.IntegerField(required=True, max_value=settings.MAX_TIME_STEPS, allow_null=True)
    end_work_time_step = validators.IntegerField(required=True, max_value=settings.MAX_TIME_STEPS, allow_null=True)
    is_day_off = validators.BooleanField(required=False)
    breaks = StaffBreakValidator(many=True, required=False)
    
    def validate(self, attrs: Any) -> Any:
        breaks = attrs.get('breaks', [])
        
        if attrs['is_day_off'] == True and len(breaks) > 0:
            raise ValidationError('Day off cannot have breaks.')
        
        if attrs['is_day_off'] == False \
            and attrs['start_work_time_step'] == attrs['end_work_time_step']:
                raise ValidationError('Start and end work time steps cannot be equal.')
        
        return super().validate(attrs)
    

class StaffScheduleValidator(validators.Validator):
    schedule = ScheduleValidator(many=True, required=True)
    
    class Meta:
        fields = [
            'schedule'
        ]