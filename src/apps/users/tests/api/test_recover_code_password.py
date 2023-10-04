import pytest
from dateutil import relativedelta

from django.utils import timezone

from apps.users.models import User, AsyncCodeOperation

from randevu.generator import generate_code


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='keks', is_active=True)


@pytest.fixture
def operation(mixer, owner):
    return mixer.blend(
        'users.AsyncCodeOperation',
        user = owner,
        code = generate_code(),
        status = AsyncCodeOperation.WAITING,
        type = AsyncCodeOperation.PASSWORD_RECOVERY,
        expire_date = timezone.now() + relativedelta.relativedelta(minutes=20)
    )


@pytest.fixture
def payload(operation):
    return {
        "code": operation.code,
    }


def test_recover_code(anon, payload):
    anon.post('/api/v2/auth/recover/check-code/', payload, expected_status_code=200)
