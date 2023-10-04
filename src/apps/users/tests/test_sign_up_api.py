import pytest
from apps.users.models import User
from apps.utils import get_or_none


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def payload():
    return {
        "password": "string",
        "sub_domain": "string",
        "login": "mmm.marchuk@mail.ru"
    }


# def test_user_registration(anon, payload):
#     anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=201)

#     user: User = get_or_none(User, email=payload['login'])

#     operations = user.get_async_operations()
#     assert user
#     assert len(operations) == 1