from enum import auto
import pytest
from django.core.cache import cache

pytest_plugins = [
    'randevu.fixtures',
    'apps.schedule.factory',
    'apps.users.factory',
    'apps.appointment.factory'
]


@pytest.fixture(autouse=True)
def _cache(request: pytest.FixtureRequest):
    """Clear django cache after each test run"""
    yield
    cache.clear()