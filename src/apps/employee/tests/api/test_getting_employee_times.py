# import pytest

# from apps.users.models import User
# pytestmark = [
#     pytest.mark.django_db
# ]


# @pytest.fixture
# def service(mixer):
#     return mixer.blend('service.SalonService')


# @pytest.fixture
# def employee(mixer, service):
#     user = mixer.blend('users.User', role=User.ADMIN, status=User.WORKING)
#     user.services.add(service)
#     user.save()
#     return user


# @pytest.fixture
# def payload(service, employee):
#     return {
#         "service_id": service.pkid,
#         "employee_id": employee.pkid,
#         "month": 12,
#         "year": 2022
#     }


# def test_employee_times(anon, employee, service):
#     got = anon.get('/api/v2/employee/times', expected_status_code=200)

#     assert got[0]['pkid'] == employee.pkid
#     assert got[0]['role'] == employee.role
#     assert got[0]['name'] == employee.name
#     assert got[0]['email'] == employee.email
#     assert got[0]['phone'] == employee.phone
#     assert got[0]['image'] == employee.image
#     assert got[0]['status'] == employee.status
#     assert got[0]['is_owner'] == employee.is_owner
#     assert got[0]['services'][0]['pkid'] == service.pkid


# def test_employee_by_service_id_list(anon, employee, service):
#     got = anon.get('/api/v2/employees/?service_id', expected_status_code=200)

#     assert got[0]['pkid'] == employee.pkid
#     assert got[0]['role'] == employee.role
#     assert got[0]['name'] == employee.name
#     assert got[0]['email'] == employee.email
#     assert got[0]['phone'] == employee.phone
#     assert got[0]['image'] == employee.image
#     assert got[0]['status'] == employee.status
#     assert got[0]['is_owner'] == employee.is_owner
#     assert got[0]['services'][0]['pkid'] == service.pkid