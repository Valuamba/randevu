from typing import Any

from apps.client.models import Client


class ClientCreator:
    def __init__(self, name: str, phone: str, company) -> None:
        self.name = name
        self.phone = phone
        self.company = company

    def __call__(self, *args: Any, **kwds: Any) -> Client:
        return Client.objects.create(
            name=self.name,
            phone=self.phone,
            company = self.company
        )