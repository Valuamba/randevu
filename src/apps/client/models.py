from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class ClientQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(company=user.company)


ClientManager = models.Manager.from_queryset(ClientQuerySet)


class Client(TimeStampedUUIDModel):
    objects = ClientManager()

    name = models.CharField(verbose_name=_('Full name'), max_length=150, blank=False, null=False)
    phone = PhoneNumberField(blank=False, db_index=True, unique=True)
    email = models.CharField(verbose_name=_('Email'), unique=True, max_length=200, null=True)
    whatsapp = models.BooleanField(verbose_name=_('WhatsApp'), default=False)
    notes = models.CharField(verbose_name=_('Notes'), max_length=300, blank=True, null=True)
    
    is_deleted = models.BooleanField(default=False)

    company = models.ForeignKey("multilanding.Multilanding", related_name='clients', on_delete=models.PROTECT, null=True)

    @property
    def contacts(self):
        return {
            'phone': self.phone,
            'email': self.email,
            'whatsapp': self.whatsapp
        }

    @property
    def appointments_statistic(self):
        appointments = self.appointments.all()

        total_price = sum([appointment.service.price for appointment in appointments], 0)
        return {
            'count':len(appointments),
            'total_price': total_price
        }
    
    class Meta:
        db_table = 'clients'
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        
    def __str__(self):
        return self.name
    