import pytest

from apps.client.models import Client
from randevu.test.api_client import DRFClient

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def employee(factory):
    return factory.employee()


@pytest.fixture
def api(employee):
    return DRFClient(user=employee, god_mode=False, anon=False)


@pytest.fixture
def payload():
    return {
        'name': 'Denis',
        'notes': 'Some notes',
        'contacts': {
            'phone': '+375298213275',
            'email': 'denis@kovalev.com',
            'whatsapp': True
        }
    }


def test_client_creation(api, payload):
    api.post('/api/v2/client/create', payload, expected_status_code=201)

    client = Client.objects.last()

    assert client.name == payload['name']
    assert client.notes == payload['notes']
    assert client.phone == payload['contacts']['phone']
    assert client.email == payload['contacts']['email']
    assert client.whatsapp == payload['contacts']['whatsapp']
