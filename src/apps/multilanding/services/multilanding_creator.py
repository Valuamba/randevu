
from apps.users.models import User
from apps.multilanding.models import Multilanding, MultilandingDomain
from apps.utils import get_or_none
from apps.multilanding.ecxeptions import SubdomainIsAlreadyUsed, IncorrectSubDomain, APIException
from apps.cloudfare.dns_client import CloudfareDNSZoneClient

from django.conf import settings
from django.db.models import Q

from typing import Any
import logging
import re
import requests
import json


logger = logging.getLogger(__name__)


class MultilandingCreator:

    def __init__(self, sub_domain: str, user: User) -> None:
        self.sub_domain = sub_domain
        self.user = user
        self.dns_client = CloudfareDNSZoneClient()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        sub_domain = self.sub_domain
        user = self.user

        if self.validate_domain(sub_domain):
            domain = MultilandingDomain.objects.get(domain=settings.RANDEVU_DOMAIN)
            multilanding = get_or_none(Multilanding, employees=user, employees__is_owner=True)

            if not multilanding:
                logger.info(f'Creating: {user}')
                if not self.check_cloudfare_zone(sub_domain) or not self.check_domain_in_db(sub_domain, user):
                        raise SubdomainIsAlreadyUsed(f'Sub domain {sub_domain} already exist.')
                self.create(sub_domain, user, domain)
            else:
                logger.info('Updating')
                if multilanding.sub_domain != sub_domain:
                    if not self.check_cloudfare_zone(sub_domain) or not self.check_domain_in_db(sub_domain, user):
                        raise SubdomainIsAlreadyUsed(f'Sub domain {sub_domain} already exist.')

                    self.update_domain(multilanding, sub_domain)
        else:
            raise Exception('Domain not correct or already used.')
        
    def validate_domain(self, sub_domain):
        if not re.match('^[a-zA-Z]+$', sub_domain):
            raise IncorrectSubDomain()

        return True
        
    def check_cloudfare_zone(self, sub_domain):
        response = self.dns_client.get_records(sub_domain)
        return len(response['result']) == 0

    def check_domain_in_db(self, sub_domain, user):
        # domain exists - you owner - domain not active - ok
        # domain exists - you owner - domain active - error
        # domain exists - you not owner - error
        # domain doesn't exist - ok

        # owner_query = Q(sub_domain=sub_domain, employees=user)
        foregin_query = Q(sub_domain=sub_domain) & ~Q(employees=user)
        
        multilandings = Multilanding.objects.filter(foregin_query)

        return len(multilandings) == 0

    def create(self, sub_domain: str, user: User, domain: MultilandingDomain):
        logger.info(f'Create multilanding {sub_domain} for user {user.email}')

        response = self.dns_client.create(sub_domain)
        multilanding = Multilanding.objects.create(
            domain = domain,
            sub_domain=sub_domain,
            dns_zone_id = response['result']['id']
        )
        user.company = multilanding
        user.save()

    def update_domain(self, multilanding: Multilanding, sub_domain: str):
        logger.info(f'Update multilanding {sub_domain}')

        self.dns_client.update_name(sub_domain, multilanding.dns_zone_id)

        multilanding.sub_domain = sub_domain
        multilanding.save()


