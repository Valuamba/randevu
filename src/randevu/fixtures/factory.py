import pytest

from randevu.test.factory import FixtureFactory
from randevu.test.mixer import mixer as _mixer


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def factory():
    return FixtureFactory()