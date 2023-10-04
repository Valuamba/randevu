from typing import Any

from apps.client.models import Client


class ClientUpdator:
    def __init__(self, client: Client, name: str, phone: str) -> None:
        self.client = client
        self.name = name
        self.phone = phone

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.client.name = self.name
        self.client.phone = self.phone

        self.client.save()

        self.client.refresh_from_db()

        return self.client