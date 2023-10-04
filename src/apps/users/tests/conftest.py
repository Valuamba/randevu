import pytest


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture(autouse=True)
def _change_cloudfare_credentials(settings):
    settings.CLOUDFARE_ACCOUNT_HASH = 'dfvfdvdffdvd'
    settings.CLOUDFARE_ACCOUNT_ID = 'fgbgfbgfbfgb34fc34c'
    settings.CLOUDFARE_API_TOKEN = 'v34vvdfvdfbvVV'
    settings.CLOUDFARE_DNS_API_TOKEN = 'Odffvdfd'
    settings.CLOUDFARE_RANDEVU_ZONE = '9d361a9bddfvdf6000f5154f2d4994'
    settings.CLOUDFARE_ZONE_CONTENT = '127.0.0.1'