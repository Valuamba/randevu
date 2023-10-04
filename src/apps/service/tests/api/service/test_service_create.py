import pytest

from apps.service.models import SalonService
from apps.locales.models import MultilandingLocale

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def payload(category):
    return {
        "category": {
            'pkid': category.pkid
        },
        "duration": 2,
        "gender": 1,
        "price": 100,
        "image": "csdcsd-23d2",
        "name": {
            "en": "Английский",
            "de": "Немецкий"
        },
        "description": {
            "ru": "Русский",
            "tr": "Турецкий",
        }
    }


def test_creation(api, payload, owner):
    api.post('/api/v2/service/create', payload, expected_status_code=201)

    service = SalonService.objects.last()

    assert service.duration == 2
    assert service.gender == 1
    assert service.price == 100
    assert service.image == 'csdcsd-23d2'
    assert service.name['de'] == 'Немецкий'
    assert service.name['en'] == 'Английский'
    assert service.description['ru'] == 'Русский'
    assert service.description['tr'] == 'Турецкий'
    assert service.company == owner.company
