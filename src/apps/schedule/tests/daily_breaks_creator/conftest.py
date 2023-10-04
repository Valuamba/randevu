from apps.schedule.services import DailyBreaksCreator
import pytest


@pytest.fixture
def create():
    return lambda *args, **kwargs: DailyBreaksCreator(*args, **kwargs)()