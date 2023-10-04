import pytest

from apps.locales.models import MultilandingLocale

from django.db.utils import IntegrityError

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def multilanding(mixer):
    return mixer.blend('multilanding.Multilanding')


@pytest.fixture
def service(mixer):
    return mixer.blend('service.SalonService')


@pytest.fixture
def category(mixer):
    return mixer.blend('service.Category')



def test_multiple_locale_entities(multilanding, service, category):
    with pytest.raises(IntegrityError):
        MultilandingLocale.objects.create(multilanding=multilanding, salon_service=service, alias='name', lang='ru')


def test_one_locale_entity(multilanding):
    locale = MultilandingLocale.objects.create(multilanding=multilanding, alias='name', lang='ru')

    assert locale


def test_ununiqie_locale_property(multilanding):
    with pytest.raises(IntegrityError):
        MultilandingLocale.objects.create(multilanding=multilanding, alias='name', lang='ru', text='2')
        MultilandingLocale.objects.create(multilanding=multilanding, alias='name', lang='ru', text='1')


def test_unique_locale_property(multilanding):
    MultilandingLocale.objects.create(multilanding=multilanding, alias='name', lang='ru', text='2')
    MultilandingLocale.objects.create(multilanding=multilanding, alias='name', lang='tr', text='1')


