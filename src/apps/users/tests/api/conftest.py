import pytest

from django.conf import settings


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture(autouse=True)
def domain(mixer):
    return mixer.blend('multilanding.MultilandingDomain', domain=settings.RANDEVU_DOMAIN)