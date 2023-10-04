from typing import Any

from django.utils import timezone
from apps.appointment.models import Appointment

from apps.common.models import TimeStampedUUIDModel
from apps.users.models import User
from apps.service.models import Category, SalonService
from apps.client.models import Client
from apps.multilanding.models import Multilanding

import logging


logger = logging.getLogger(__name__)


class AppointmentCreator:
    
    def __init__(self, service: SalonService, employee: User, \
        category: Category, client: dict, day: str, time_step: int,\
        company: Multilanding) -> None:
        self.service = service
        self.employee = employee
        self.category = category
        self.client = client
        self.day = day
        self.time_step = time_step
        self.company = company
    
    def __call__(self, *args: Any, **kwds: Any) -> Appointment:
        logger.info(f'Create appointment by employee {self.employee.email}')
        return self.create()

    def create(self) -> Appointment:
        appointment = Appointment.objects.create(
            service=self.service,
            client=self.client,
            employee=self.employee,
            category=self.category,
            day=self.day,
            time_step=self.time_step,
            company = self.company
        )
        return appointment