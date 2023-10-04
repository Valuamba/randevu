
import pytest

from rest_framework.request import Request

from django.http import HttpRequest
from django.conf import settings

from randevu.test.api_client import DRFClient


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def multilanding(mixer):
    return mixer.blend('multilanding.Multilanding', 
        sub_domain='littlebarber',
        country='Brasil',
        city='Minsk',
        street='lenina',
        building='s12',
        googleMapApiKey='oneTwoThreeFore',
        phone='+48123456789',
        facebook='Kokos@smile.ru',
        instagram='HotRandevu',
        whatsapp='MylittlePony',
        start_work_week_day=2,
        end_work_week_day=5,
        start_work_time_step=30,
        end_work_time_step=80,
        cover='sd8dcsd78v7sdvdsvsd8',
        gallery=[]
    )


@pytest.fixture
def owner(factory, multilanding):
    return factory.owner(multilanding=multilanding, is_active=True)


@pytest.fixture
def api(owner):
    return DRFClient(user=owner, god_mode=False, anon=False)


@pytest.fixture
def paylaod():
    return {
            'name': {
                'en': 'Name',
                'ru': 'Имя',
                'tr': 'Namio',
                'de': 'Nashs'
            },
            'description': {
                'en': 'Description',
                'ru': 'Описание',
                'tr': 'Desvsvd',
                'de': 'fdbvfdb',
            },
            'location': {
                'country': 'UAE',
                'city': 'Dubai',
                'street': 'Lenina',
                'building': '32',

                'gmapApiKey': 'oneTwoThreeFore'
            },
            'schedule': {
                'days': [4, 7],
                'intervals': [50, 80],
            },
            'contacts': {
                'phone': '+48123456789',
                'facebook': 'Kokos@smile.ru', 
                'instagram': 'HotRandevu',
                'whatsapp': 'MylittlePony'
            },

            'cover': 'cover.img',
            'gallery': [
                'some.img',
                'second.img'
            ]
        }


def test_webiste_update(api, paylaod, multilanding):
    api.put('/api/v2/website/update', paylaod, expected_status_code = 200)

    multilanding.refresh_from_db()

    assert paylaod['schedule']['days'][0] == multilanding.start_work_week_day
    assert paylaod['schedule']['days'][1] == multilanding.end_work_week_day

    assert paylaod['schedule']['intervals'][0] == multilanding.start_work_time_step
    assert paylaod['schedule']['intervals'][1] == multilanding.end_work_time_step

    assert paylaod['location']['gmapApiKey'] == multilanding.googleMapApiKey
    assert paylaod['location']['country'] == multilanding.country
    assert paylaod['location']['city'] == multilanding.city
    assert paylaod['location']['street'] == multilanding.street
    assert paylaod['location']['building'] == multilanding.building

    assert paylaod['contacts']['facebook'] == multilanding.facebook
    assert paylaod['contacts']['instagram'] == multilanding.instagram
    assert paylaod['contacts']['whatsapp'] == multilanding.whatsapp
    assert paylaod['contacts']['phone'] == multilanding.phone

    assert paylaod['cover'] == multilanding.cover
    assert paylaod['gallery'] == multilanding.gallery