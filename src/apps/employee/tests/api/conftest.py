import pytest

from randevu.test.api_client import DRFClient
from apps.users.models import User

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='mylittlepony', is_active=True, is_staff=False, \
        is_superuser=False)


@pytest.fixture
def admin(factory):
    return factory.admin()


@pytest.fixture
def api(admin):
    return DRFClient(user=admin, god_mode=False, anon=False)