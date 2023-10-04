import pytest


pytestmark = [
    pytest.mark.django_db
]



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


@pytest.fixture
def client(mixer, employee):
    return mixer.blend('client.Client', is_deleted=False, company=employee.company)


def test_client_update(api, client, payload):
    api.put(f'/api/v2/client/{client.pkid}/update', payload)

    client.refresh_from_db()

    assert client.name == payload['name']
    assert client.notes == payload['notes']
    assert client.email == payload['contacts']['email']
    assert client.phone == payload['contacts']['phone']
    assert client.whatsapp == payload['contacts']['whatsapp']
