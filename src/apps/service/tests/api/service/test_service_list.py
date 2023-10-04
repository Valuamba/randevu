import pytest

from apps.service.models import SalonService
from apps.locales.models import MultilandingLocale
from apps.users.models import User

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def employee(mixer):
    return mixer.blend('users.User', role=User.EMPLOYEE, status=User.WORKING)


@pytest.fixture
def service(mixer, category, employee, owner):
    service = mixer.blend('service.SalonService', company=owner.company)
    service.category = category

    service.employees.add(employee)

    service.save()
    return service


def test_list(api, service, employee):
    got = api.get('/api/v2/services/', expected_status_code=200)   

    db_service = got[-1]

    assert db_service['duration'] == service.duration
    assert db_service['gender'] == service.gender
    assert db_service['price'] == service.price
    assert db_service['image'] == service.image
    assert db_service['name'] == service.name
    assert db_service['description'] == service.description
    assert len(db_service['employees']) == 1


def test_filter_by_category_creation(api, service, category):
    got = api.get(f'/api/v2/services/?category_id={category.pkid}', expected_status_code=200)   

    db_service = got[-1]

    assert db_service['duration'] == service.duration
    assert db_service['gender'] == service.gender
    assert db_service['price'] == service.price
    assert db_service['image'] == service.image
    assert db_service['name'] == service.name
    assert db_service['description'] == service.description