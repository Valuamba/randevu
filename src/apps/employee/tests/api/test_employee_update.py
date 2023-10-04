import pytest
import uuid

from apps.users.models.user import User

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def employee(mixer, admin):
    return mixer.blend('users.User', company=admin.company,  role=User.ADMIN, status=User.WORKING)


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService')


@pytest.fixture
def payload(service, employee):
    return {
        'role': User.ADMIN,
        'name': employee.name,
        'email': 'kaban@les.com',
        'phone': '+48731331105',
        'image': 'sdfds-sdfds',
        'status': User.NOT_WORKING,
        'services': [ service.pkid ]
    }


def test_employee_update(api, payload, employee, service, admin):
    api.put(f'/api/v2/employee/{employee.pkid}/update/', payload, expected_status_code=200)

    employee.refresh_from_db()

    assert employee.role == User.ADMIN
    assert employee.name == employee.name
    assert employee.email == 'kaban@les.com'
    assert employee.phone == '+48731331105'
    assert employee.image == 'sdfds-sdfds'
    assert employee.status == User.NOT_WORKING
    assert employee.services.last().pkid == service.pkid

    assert employee.company == admin.company