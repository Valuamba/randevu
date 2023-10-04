
from typing import Any

from apps.cloudfare.dns_client import CloudfareDNSZoneClient


class CloudfareDNSCreator:
    def __init__(self, zone_name: str, multilanding_id: int) -> None:
        self.zone_name = zone_name
        self.multilanding_id = multilanding_id

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        dns_client = CloudfareDNSZoneClient()

        response = dns_client.get_records(self.zone_name)

        if len(response['result']) > 0:
            raise Exception(f'Record with zone {self.zone_name} already exist.')

        dns_client.create(self.zone_name)