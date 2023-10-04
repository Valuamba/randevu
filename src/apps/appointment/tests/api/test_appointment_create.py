import pytest

from apps.appointment.models import Appointment
from apps.client.models import Client


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def category(mixer):
    return mixer.blend('service.Category')


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService')


@pytest.fixture
def payload(service, employee, category):
    return {
        'service': {
            'id': service.pkid
        },
        'employee': {
            'id': employee.pkid
        },
        'category': {
            'id': category.pkid
        },
        'client': {
            'name': 'Benedikt Kaberbetch',
            'phone': '+48731331105'
        },
        'date': {
            'day': '2022-12-02',
            'time_step': 45
        }
    }


def test_appointment_create(api, payload, service, employee):
    api.post('/api/v2/appointment/create', payload, expected_status_code=201)

    appointment = Appointment.objects.last()
    client = Client.objects.last()

    assert appointment.service == service
    assert appointment.employee == employee
    assert appointment.client == client
    assert appointment.day.strftime('%Y-%m-%d') == payload['date']['day']
    assert appointment.time_step == payload['date']['time_step']
