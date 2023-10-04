import pytest

from apps.service.models import Category
from apps.locales.models import MultilandingLocale

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def payload():
    return {
        'image': 'img',
        'name': {
            'en': 'lol',
            'ru': 'string',
            'tr': 'string',
            'de': 'string',
        },
        'description': {
            'en': 'kek',
            'ru': 'string',
            'tr': 'string',
            'de': 'string'
        }
    }


def test_create_category(api, payload, employee):
    response = api.post('/api/v2/category/create', payload, expected_status_code=201)

    category = Category.objects.last()
    locales = MultilandingLocale.objects.all()

    assert 'body' not in response.keys()
    assert category.id is not None
    assert category.pkid is not None
    assert category.image == 'img'
    assert category.services.count() == 0

    assert len(locales) == 8
    assert category.name['en'] == 'lol'
    assert category.description ['en'] == 'kek'

    assert category.company == employee.company