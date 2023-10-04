import pytest

from django.contrib.auth import authenticate


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='keks', password='12354', is_active=True)


@pytest.fixture
def payload(owner):
    return {
        "login": owner.email,
        "password": "secret"
    }


def test_edit_new_password(anon, payload, owner):
    anon.post('/api/v2/auth/recover/edit-password/', payload, expected_status_code=200)

    authenticate_kwargs = {
        'email': owner.email,
        'password': 'secret',
    }

    user = authenticate(**authenticate_kwargs)

    assert user != None
