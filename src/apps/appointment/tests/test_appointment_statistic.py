import pytest

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService', price=200)


@pytest.fixture
def appointment(mixer, service, client):
    return mixer.blend('appointment.Appointment', service=service, client=client)


@pytest.fixture
def client(mixer):
    return mixer.blend('client.Client')


def test_appointment_statistic(appointment, client):
    result = client.appointments_statistic

    assert result['count'] == 1
    assert result['total_price'] == 200
