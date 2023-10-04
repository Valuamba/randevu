from rest_framework.test import APIClient
from mixer.backend.django import mixer as _mixer
import pytest
from django.conf import settings


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def domain(mixer):
    return mixer.blend('multilanding.MultilandingDomain', domain=settings.RANDEVU_DOMAIN)


@pytest.fixture
def user(mixer):
    return mixer.blend('users.User')


# @pytest.fixture(autouse=True)
# def trigger(mocker, mixer):
#     mock_requests = mocker.patch("requests.get")
#     mock_requests.return_value.ok = True
    
#     return mock_requests

# @pytest.fixture
# def multilanding(mixer):
#     return mixer.blend('multilanding.Multilanding', sub_domian='mysweetbarber', user_id=12)