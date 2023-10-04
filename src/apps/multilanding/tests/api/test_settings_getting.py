import pytest

from randevu.test.api_client import DRFClient

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def owner(factory):
    return factory.owner(sub_domain='mybarber', is_active=True)


@pytest.fixture
def api(owner):
    return DRFClient(user=owner, god_mode=False, anon=False)


def test_settings_getting(api, owner):
    got = api.get('/api/v2/settings', expected_status_code=200)

    localization = got['localization']
    
    assert localization['default'] == owner.company.default_lang
    assert localization['active'] == owner.company.langs