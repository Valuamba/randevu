import pytest

from apps.users.models import User, AsyncCodeOperation


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='keks', code=676748, is_active=False)


@pytest.fixture
def payload(owner):
    return {
        "code": 676748,
        "login": owner.email
    }


def test_verification_registration(anon, payload, owner):
    anon.post('/api/v2/auth/sign-up/verify/', payload, expected_status_code=200)

    owner.refresh_from_db()

    operation = AsyncCodeOperation.objects.get(code=676748)

    assert owner.is_active == True
    assert owner.status == User.WORKING
    assert owner.role == User.OWNER
    assert owner.is_owner == True
    assert operation.status == AsyncCodeOperation.SUCCEED

    multilanding = owner.company

    assert multilanding.sub_domain == 'keks'
    # assert multilanding.is_active == True
