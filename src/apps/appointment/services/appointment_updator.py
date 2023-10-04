from typing import Any

from django.utils import timezone
from apps.appointment.models import Appointment

from apps.common.models import TimeStampedUUIDModel
from apps.users.models import User
from apps.service.models import Category, SalonService
from apps.client.models import Client


class AppointmentUpdator:
    def __init__(self, appointment: Appointment, service: SalonService, employee: User, category: Category, client: dict, date: str, time_step: int) -> None:
        self.appointment = appointment
        self.service = service
        self.employee = employee
        self.category = category
        self.client = client
        self.date = date
        self.time_step = time_step
    
    def __call__(self, *args: Any, **kwds: Any) -> Appointment:
        appointment = self.appointment

        return self.update(appointment)

    def update(self, appointment: Appointment) -> Appointment:
        appointment.service = self.service
        appointment.employee = self.employee
        appointment.client = self.client
        appointment.day = self.date
        appointment.time_step = self.time_step

        appointment.save()

        return appointment