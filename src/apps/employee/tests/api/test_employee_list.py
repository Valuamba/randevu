import pytest

from apps.users.models import User
pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService')


@pytest.fixture
def employee(mixer, service, admin):
    user = mixer.blend('users.User', role=User.ADMIN, status=User.WORKING, company=admin.company,
        name='Some name')
    user.services.add(service)
    user.save()
    return user


def test_employee_list(api, employee, service):
    got = api.get('/api/v2/employees/', expected_status_code=200)

    db_employee = next((e for e in got if e['pkid'] == employee.pkid), None)

    # assert db_employee['pkid'] == employee.pkid
    assert db_employee['role'] == employee.role
    assert db_employee['name'] == employee.name
    assert db_employee['email'] == employee.email
    assert db_employee['phone'] == employee.phone
    assert db_employee['image'] == employee.image
    assert db_employee['status'] == employee.status
    assert db_employee['is_owner'] == employee.is_owner
    assert db_employee['services'][0]['pkid'] == service.pkid


def test_employee_by_service_id_list(api, employee, service):
    got = api.get('/api/v2/employees/?service_id', expected_status_code=200)

    db_employee = db_employee = next((e for e in got if e['pkid'] == employee.pkid), None)

    # assert db_employee['pkid'] == employee.pkid
    assert db_employee['role'] == employee.role
    assert db_employee['name'] == employee.name
    assert db_employee['email'] == employee.email
    assert db_employee['phone'] == employee.phone
    assert db_employee['image'] == employee.image
    assert db_employee['status'] == employee.status
    assert db_employee['is_owner'] == employee.is_owner
    assert db_employee['services'][0]['pkid'] == service.pkid