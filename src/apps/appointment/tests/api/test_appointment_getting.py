import pytest 

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def employee(factory):
    return factory.employee()


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


def test_appointment(api, appointment, employee, payload):
    got = api.get('/api/v2/appointments/', payload=payload, expected_status_code=200)

    db_appointment = got[-1]

    assert db_appointment['date']['day'] == appointment.day.strftime('%Y-%m-%d')
    assert db_appointment['index'] == appointment.index
    assert db_appointment['status'] == appointment.status
    assert db_appointment['employee']['email'] == employee.email
    assert db_appointment['client']['phone'] == appointment.client.phone
    assert db_appointment['service']['image'] == appointment.service.image
