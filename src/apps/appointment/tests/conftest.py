import pytest


@pytest.fixture
def employee(mixer):
    return mixer.blend('users.User', pkid=2, name='Авраам Соломонович Пейзенгольц', email='abraham@gmail.com')


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService', pkid=3)


@pytest.fixture
def category(mixer):
    return mixer.blend('service.Category', pkid=1)