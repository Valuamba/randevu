import pytest

from apps.users.models import User, AsyncCodeOperation

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='keks', password='secret', is_active=True)


@pytest.fixture
def not_active_owner(owner):
    owner.is_active = False
    owner.save()


@pytest.fixture
def payload(owner):
    return {
        "password": 'secret',
        "login": owner.email
    }


def test_sign_in(anon, payload, owner):
    got = anon.post('/api/v2/auth/sign-in/', payload, expected_status_code=200)

    assert got['jwt']
    assert got['user_id'] == owner.pkid
    assert got['user_role'] == owner.role


def test_sign_in(anon, payload, not_active_owner):
    anon.post('/api/v2/auth/sign-in/', payload, expected_status_code=401)
