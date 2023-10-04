import pytest
import uuid


from apps.users.models.user import User

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def employee(mixer):
    return mixer.blend('users.User')


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService')


@pytest.fixture
def payload(service, employee):
    return {
        'role': User.EMPLOYEE,
        'name': employee.name,
        'email': 'kaban@les.com',
        'phone': employee.phone,
        'image': employee.image,
        'status': User.WORKING,
        'services': [ service.pkid ]
    }


def test_employee_create(api, payload, employee, service, admin):
    got = api.post('/api/v2/employee/create/', payload, expected_status_code=201)

    new_employee = User.objects.last()

    assert new_employee.role == User.EMPLOYEE
    assert new_employee.name == employee.name
    assert new_employee.email == 'kaban@les.com'
    assert new_employee.phone == employee.phone
    assert new_employee.image == employee.image
    assert new_employee.status == User.WORKING
    assert new_employee.services.first() == service
    assert new_employee.company == admin.company
    assert got['pkid'] == new_employee.pkid