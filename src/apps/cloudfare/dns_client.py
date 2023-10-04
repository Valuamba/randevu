import httpx
from urllib.parse import urljoin
import json

from django.conf import settings

from apps.cloudfare.exceptions import HTTPError


class CloudfareDNSZoneClient:
    def get_records(self, zone_name: str) -> dict:
        zone = f'{zone_name}.{settings.RANDEVU_DOMAIN}'
        response = self.fetch(
            method=f'dns_records?type=A&name={zone}'
        )
        return response

    def update_name(self, zone_name: str, id: str) -> dict:
        response = self.patch(
            method=f'dns_records/{id}',
            payload={
                'name': f'{zone_name}.{settings.RANDEVU_DOMAIN}'
            }
        )
        return response

    def create(self, zone_name: str) -> dict:
        response = self.post(
            method='dns_records',
            payload={
                'type': 'A',
                'name': f'{zone_name}.{settings.RANDEVU_DOMAIN}',
                'content': settings.CLOUDFARE_ZONE_CONTENT,
                'ttl': 3600,
                'priority': 10,
                'proxied': False
            }
        )
        return response

    def patch(self, method: str, payload: dict) -> dict:
        response = httpx.patch(
            url=urljoin(settings.CLOUDFARE_BASE_URL, f'zones/{settings.CLOUDFARE_RANDEVU_ZONE}/{method}'),
            json=payload,
            headers={
                'Authorization': f'Bearer {settings.CLOUDFARE_DNS_API_TOKEN}',
            },
        )

        if response.status_code != 200:
            data = response.json()
            error = data['errors']
            raise HTTPError('Cloudfare DNS HTTP %s, error: %s (code: %s)', response.status_code, error['message'], error['code'])

        return response.json()

    def post(self, method: str, payload: dict) -> dict:
        response = httpx.post(
            url=urljoin(settings.CLOUDFARE_BASE_URL, f'zones/{settings.CLOUDFARE_RANDEVU_ZONE}/{method}'),
            json=payload,
            headers={
                'Authorization': f'Bearer {settings.CLOUDFARE_DNS_API_TOKEN}',
            },
        )

        if response.status_code not in [200, 201]:
            data = response.json()
            raise HTTPError('Cloudfare DNS HTTP %s, error: %s (code: %s)', response.status_code, data['error']['text'], data['error']['error_id'])

        return response.json()

    def fetch(self, method: str):
        # url = 'https://api.cloudflare.com/client/v4/zones/9d361a9bd2b5eefd6000f5154f2d4994/dns_records?type=A&name=randevu.beauty'

        url = urljoin(settings.CLOUDFARE_BASE_URL, f'zones/{settings.CLOUDFARE_RANDEVU_ZONE}/{method}')
        response = httpx.get(
            url=url,
            headers={
                'Authorization': f'Bearer {settings.CLOUDFARE_DNS_API_TOKEN}',
            })

        if response.status_code != 200:
            raise HTTPError(f'HTTP Error {response.status_code} fetching cloudfare resouce {method}: {response.text}')

        return response.json()
