from datetime import timedelta
from typing import List

from django.conf import settings


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def present_time_slots_with_label(slots: List[int]):
    labeled_slots = []
    for slot in slots:
        labeled_slots.append({
            'value': slot,
            'label': ':'.join(str(timedelta(minutes=slot * settings.TIME_STEP_MINUTES)).split(':')[:2])
        })
    return labeled_slots