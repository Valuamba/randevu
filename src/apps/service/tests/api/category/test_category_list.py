import pytest

from apps.service.models import Category
from apps.locales.models import MultilandingLocale


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def category(mixer, employee):
    return mixer.blend('service.Category', company=employee.company)


@pytest.fixture
def payload():
    return {
        'count': 10,
        'page': 1
    }


def test(api, payload, category):
    got = api.get('/api/v2/categories/?page=1&count=10', payload, expected_status_code=200)

    assert len(got) == 1
    assert got[0]['image'] == category.image
    assert len(got[0]['services']) == 0


def test_category_list(api, payload, category):
    got = api.get('/api/v2/categories/?page=1&count=10', expected_status_code=200)

    assert len(got) == 1
    assert got[0]['image'] == category.image
    assert len(got[0]['services']) == 0