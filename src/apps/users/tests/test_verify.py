import pytest
from apps.users.models import User, AsyncCodeOperation
from apps.utils import get_or_none

from django.utils import timezone
from dateutil.relativedelta import relativedelta


pytestmark = [
    pytest.mark.django_db
]

@pytest.fixture
def user(mixer):
    return mixer.blend('users.User', email='kok@coock.com', password='xxxTentacion', is_active=False)


@pytest.fixture
def async_operation(mixer, user):
    code = mixer.blend('users.AsyncCodeOperation', user=user, \
        expire_date=timezone.now() + relativedelta(minutes=20))
    return code


@pytest.fixture
def payload(user, async_operation):
    return {
        "code": async_operation.code,
        "login": user.email
    }


def test_user_registration_code_verification(anon, async_operation, user, payload):
    anon.post('/api/v2/auth/sign-up/verify/', payload, expected_status_code=200)

    async_operation.refresh_from_db()
    user.refresh_from_db()

    operations = user.get_async_operations()

    assert user.is_active == True
    assert len(operations) == 1
    assert async_operation.status == AsyncCodeOperation.SUCCEED
