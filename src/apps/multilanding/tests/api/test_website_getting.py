
import pytest

from rest_framework.request import Request

from django.http import HttpRequest
from django.conf import settings


pytestmark = [
    pytest.mark.django_db
]


# @pytest.fixture(autouse=True)
# def add_sub_domain_to_absolute_url(mocker, multilanding):
#     return mocker.patch('django.http.HttpRequest.build_absolute_uri', 
#         return_value=f'http://{multilanding.sub_domain}.testserver/api/v2/website')


# @pytest.fixture
# def dns_zone_middleware(mocker):
#     return mocker.patch('randevu.middlewares.DnsZoneMiddleware.__call__')


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


def test_website_getting(anon, multilanding):

    got = anon.get('/api/v2/website', expected_status_code = 200,
        **{ 'HTTP_SFC_DNS_ZONE': multilanding.sub_domain }
    )

    assert got['schedule']['days'][0] == multilanding.start_work_week_day
    assert got['schedule']['days'][1] == multilanding.end_work_week_day

    assert got['schedule']['intervals'][0] == multilanding.start_work_time_step
    assert got['schedule']['intervals'][1] == multilanding.end_work_time_step

    assert got['cover'] == multilanding.cover
    assert got['gallery'] == multilanding.gallery

    assert got['location']['gmapApiKey'] == multilanding.googleMapApiKey
    assert got['location']['country'] == multilanding.country
    assert got['location']['city'] == multilanding.city
    assert got['location']['street'] == multilanding.street
    assert got['location']['building'] == multilanding.building

    assert got['contacts']['facebook'] == multilanding.facebook
    assert got['contacts']['instagram'] == multilanding.instagram
    assert got['contacts']['whatsapp'] == multilanding.whatsapp
    # assert got['contacts']['phone'] == multilanding.phone