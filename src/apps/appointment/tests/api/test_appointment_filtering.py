import pytest 

from apps.appointment.models import Appointment

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def client(mixer):
    return mixer.blend('client.Client', name='Иосиф Кабзонович', phone='+6285695911190')


@pytest.fixture
def appointment(factory, employee, client):
    return factory.appointment(employee, client=client, company=employee.company)


@pytest.fixture
def payload():
    return {
        'page': 1,
        'count': 2,
        'interval': 3,
        'status': 0
    }


def test_search(api, appointment, payload):
    got = api.get('/api/v2/appointments/?search=иосиф', payload=payload, expected_status_code=200)

    assert got[0]['client']['name'] == appointment.client.name


def test_search_invalid(api, appointment, payload):
    got = api.get('/api/v2/appointments/?search=дональд', payload=payload, expected_status_code=200)

    assert len(got) == 0


def test_filter_by_employee(api, appointment, payload):
    got = api.get(f'/api/v2/appointments/?employee={appointment.employee.pkid}', payload=payload, expected_status_code=200)

    assert len(got) == 1


def test_filter_by_status(api, appointment, payload):
    got = api.get(f'/api/v2/appointments/?status={Appointment.CANCELED}', payload=payload, expected_status_code=200)

    assert len(got) == 0