import pytest

from apps.users.models import User
from apps.multilanding.models import MultilandingDomain, Multilanding

from django.conf import settings
from django.db.models import Q

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def valid_domain(mocker):
    return mocker.patch('apps.cloudfare.dns_client.CloudfareDNSZoneClient.get_records', return_value={
        'result': []
    })

@pytest.fixture
def already_used_domain(mocker):
    return mocker.patch('apps.cloudfare.dns_client.CloudfareDNSZoneClient.get_records', return_value={
        'result': [
            {
                'id': '2112321'
            }
        ]
    })


@pytest.fixture(autouse=True)
def register_zone(mocker):
    return mocker.patch('apps.cloudfare.dns_client.CloudfareDNSZoneClient.create', return_value={
        'result': {
            'id': '12SDS3sds2fSDdds1'
        }
    })


@pytest.fixture
def update_zone(mocker):
    return mocker.patch('apps.cloudfare.dns_client.CloudfareDNSZoneClient.update_name')


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='ronaldo', email='penalty@shtanga.com', is_active=False)


@pytest.fixture
def payload():
    return {
        "password": "kokosBugatti",
        "sub_domain": "ronaldo",
        "login": "penalty@shtanga.com"
    }


def test_registration(anon, payload, domain, valid_domain):
    anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=201)

    owner = User.objects.get(email='penalty@shtanga.com')

    assert owner.is_owner == True
    assert owner.is_active == False
    assert owner.status == User.WORKING
    assert owner.role == User.OWNER

    multilanding = owner.company

    assert multilanding.sub_domain == 'ronaldo'
    # assert multilanding.is_active == False
    assert multilanding.domain == domain


def test_used_domain(anon, payload, domain, already_used_domain):
   anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=400)


def test_re_registration_with_same_domain_and_email(anon, payload, domain, owner, valid_domain, update_zone, register_zone):
    anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=201)

    owner.refresh_from_db()

    assert owner.email == 'penalty@shtanga.com'

    update_zone.assert_not_called()
    register_zone.assert_not_called()


def test_registration_with_same_domain(anon, payload, domain, owner, valid_domain, update_zone, register_zone):
    payload['login'] = 'bekas@exchange.com'
    anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=400)


def test_update_domain(anon, payload, domain, owner, valid_domain, update_zone, register_zone):
    payload['sub_domain'] = 'crypto'
    anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=201)

    owner.refresh_from_db()

    update_zone.assert_called_once()
    register_zone.assert_not_called()

    assert owner.email == payload['login']
    assert owner.company.sub_domain == 'crypto'


def test_existing_domain_in_cloudfare(anon, payload, domain, owner, already_used_domain):
    payload['login'] = 'bekas@exchange.com'
    anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=400)


def test_existing_domain_in_database(anon, payload, domain, owner, valid_domain):
    payload['login'] = 'bekas@exchange.com'
    anon.post('/api/v2/auth/sign-up/', payload, expected_status_code=400)