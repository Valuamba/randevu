import pytest

from randevu.test.api_client import DRFClient
from apps.users.models import User

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def employee(factory):
    return factory.employee()


@pytest.fixture
def api(employee):
    return DRFClient(user=employee, god_mode=False, anon=False)
