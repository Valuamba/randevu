import pytest

from randevu.test.api_client import DRFClient

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def category(mixer, employee):
    return mixer.blend('service.Category', company=employee.company)