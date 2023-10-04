import pytest

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture(autouse=True)
def _set_time_step_range(settings):
    settings.TIME_STEP_MINUTES = 15
    settings.MAX_TIME_STEPS = int(24 * 60 / settings.TIME_STEP_MINUTES) 