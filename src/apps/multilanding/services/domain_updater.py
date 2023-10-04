from apps.multilanding.models import Multilanding
from apps.multilanding.ecxeptions import IncorrectSubDomain
from apps.users.models import User
from apps.cloudfare.dns_client import CloudfareDNSZoneClient

import re
import logging

from django.db.models import Q

logger = logging.getLogger(__name__)


class SubDomainUpdater:
    def __init__(self, sub_domain, user, dns_zone_id):
        self.sub_domain = sub_domain
        self.user = user
        self.dns_zone_id = dns_zone_id
        self.dns_client = CloudfareDNSZoneClient()

    def __call__(self, *args, **kwargs):
        self.update_domain(self.sub_domain, self.user, self.dns_zone_id)

    def update_domain(self, sub_domain: str, user: User, dns_zone_id):
        if self.validate_domain(sub_domain) and self.check_cloudfare_zone(sub_domain) \
            and self.check_domain_in_db(sub_domain, user):
            self.dns_client.update_name(sub_domain, dns_zone_id)
            logger.info(f'Domain {self.sub_domain} with dns zone {dns_zone_id} was updated.')

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
