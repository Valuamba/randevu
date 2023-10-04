import pytest


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def payload():
    return {
        'page': 1,
        'count': 2
    }


@pytest.fixture
def client(mixer, employee):
    return mixer.blend('client.Client', is_deleted=False, company=employee.company)


def test_client_list(api, payload, client):
    got = api.get('/api/v2/clients/?page=1&count=10', expected_status_code=200)

    assert len(got) == 1
    assert got[0]['appointments_statistic']
    assert got[0]['contacts']['phone'] == client.phone
    assert got[0]['contacts']['email'] == client.email
    assert got[0]['contacts']['whatsapp'] == client.whatsapp