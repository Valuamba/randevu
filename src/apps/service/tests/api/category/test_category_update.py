import pytest

from apps.service.models import Category
from apps.locales.models import MultilandingLocale

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def payload():
    return {
        'image': 'some.png',
        'name': {
            'en': 'green sheep',
            'ru': 'Зеленый луг',
        },
        'description': {
            'tr': 'avrora',
        }
    }


def test_create_category(api, payload, category, employee):
    api.put(f'/api/v2/category/{category.pkid}/update', payload, expected_status_code=200)

    category.refresh_from_db()

    locales = MultilandingLocale.objects.filter(category=category)

    assert category.image == 'some.png'
    assert category.name['en'] == 'green sheep'
    assert category.name['ru'] == 'Зеленый луг'
    assert category.description['tr'] == 'avrora'
    assert locales.count() == 3

    assert category.company == employee.company

