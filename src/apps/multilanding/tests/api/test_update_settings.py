import pytest

from randevu.test.api_client import DRFClient
from apps.multilanding.services import SubDomainUpdater

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture(autouse=True)
def cloudfare_api(mocker):
    return mocker.patch('apps.multilanding.services.SubDomainUpdater.__call__', return_value={
        'result': None
    })

@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='mybarber', is_active=True)


@pytest.fixture
def api(owner):
    return DRFClient(user=owner, god_mode=False, anon=False)


@pytest.fixture
def payload():
    return {
        'localization': {
            'default': 'ru',
            'active': [
                'ru',
                'de'
            ]
        },
        'sub_domain': 'kekcheburek'
    }

def test_settings_updating(api, owner, payload):
    api.put('/api/v2/settings/update', payload, expected_status_code=200)

    owner.company.refresh_from_db()

    localization = payload['localization']
    
    assert localization['default'] == owner.company.default_lang
    assert localization['active'] == owner.company.langs