from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_salon_service(value):
    hours = 24
    minutes_per_hour = 60
    max_time_steps_per_day = (hours * minutes_per_hour) / settings.TIME_STEP_MINUTES
    
    if value <= 0 :
        raise ValidationError(_('Duration of service cannot be less or equal to zero'))
    
    if value > max_time_steps_per_day:
        raise ValidationError(_('Duration was exceed max amount of time steps in a day.'))