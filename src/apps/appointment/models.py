from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.users.models import User
from apps.service.models import Category, SalonService
from apps.client.models import Client
# Create your models here.


class AppointmentQuerySet(models.QuerySet):
    # def for_subdomain(self, sub_domain: str):
    #     return self.filter(company__sub_domain=sub_domain)

    def for_user(self, user):
        return self.filter(company=user.company)


AppointmentManager = models.Manager.from_queryset(AppointmentQuerySet)


class Appointment(TimeStampedUUIDModel):
    objects = AppointmentManager()

    NEW = 0
    WAIT = 1
    IN_PROGRESS = 2
    DONE = 3
    CANCELED = 5

    APPOINTMENT_STATUS = [
        (NEW, "New"),
        (WAIT, "Wait"),
        (IN_PROGRESS, "In Progress"),
        (DONE, "Done"),
        (CANCELED, "Canceled")
    ]

    ALL = 0
    TODAY = 1
    WEEK = 2
    MONTH = 3

    DISPLAY_TYPES = [
        (ALL, "All"),
        (TODAY, 'Today'),
        (WEEK, 'Week'),
        (MONTH, 'Month')
    ]

    employee = models.ForeignKey(User, related_name='appointments', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='appointments', on_delete=models.PROTECT)
    service = models.ForeignKey(SalonService, related_name='appointments', on_delete=models.PROTECT)
    client = models.ForeignKey(Client, related_name='appointments', on_delete=models.PROTECT)
    
    time_step = models.IntegerField(verbose_name=_('Time step'))
    day = models.DateField(verbose_name=_('Appoinment date'), null=False, blank=False)

    status = models.IntegerField(verbose_name=_('Status'), choices=APPOINTMENT_STATUS, default=NEW)

    company = models.ForeignKey("multilanding.Multilanding", related_name='appointments', on_delete=models.PROTECT, null=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'appointment'
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
        
        constraints = [
            models.UniqueConstraint(fields=['employee', 'day', 'time_step'], name='unique_employee')
        ]
        
        indexes = [
            models.Index(fields=['employee', 'day'])
        ]
    
    @property
    def index(self):
        return 1

    @property
    def date(self):
        return {
            'day': self.day,
            'time_step': self.time_step
        }

    def get_appointment_time_range(self) -> set:
        return set(range(self.time_step, self.time_step + self.service.duration))
        
    def __str__(self) -> str:
        return f'{self.service.name}: {self.client.name}'