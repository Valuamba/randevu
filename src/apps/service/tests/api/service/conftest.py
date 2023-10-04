import pytest

from apps.users.models import User
from randevu.test.api_client import DRFClient

import uuid


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='kek', is_active=True)


@pytest.fixture
def api(owner):
    return DRFClient(user=owner, god_mode=False, anon=False)

# @pytest.fixture
# def api(api):
#     api.user.is_superuser = False
#     api.user.save()

#     return api


@pytest.fixture
def category(mixer):
    return mixer.blend('service.Category')


# @pytest.fixture
# def employee(mixer):
#     return mixer.blend('users.User', status=User.EMPLOYEE, role=User.WORKING,
#         full_name='Барабан Струнович', image=uuid.uuid4()
#     )