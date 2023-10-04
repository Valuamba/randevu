from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from apps.users.models import User
from randevu.models import TimeStampedUUIDModel, ModelWithLocales

from typing import Dict, List, Any
from datetime import timedelta

from phonenumber_field.modelfields import PhoneNumberField   


class MultilandingDomain(TimeStampedUUIDModel):
    domain = models.CharField(verbose_name='Domain', max_length=100, db_index=True, unique=True)
    
    class Meta:
        db_table = "multilanding-domains"
        
    def __str__(self) -> str:
        return self.domain        


class Multilanding(ModelWithLocales):
    NAME = "name"
    DESCRIPTION = "description"

    LOCALIZED_FIELDS = [
        (NAME, "Name"),
        (DESCRIPTION, "Description")
    ]

    country = models.CharField(verbose_name=_('Country'), max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name=_('City'), max_length=100, blank=True, null=True)
    street = models.CharField(verbose_name=_('Street'), max_length=100, blank=True, null=True)
    building = models.CharField(verbose_name=_('Building'), max_length=100, blank=True, null=True)
    googleMapApiKey = models.CharField(verbose_name=_('Google Map API key'), max_length=100, blank=True, null=True)

    phone = PhoneNumberField(null=True, blank=True)
    facebook = models.CharField(verbose_name=_('Facebook'), max_length=100, blank=True, null=True)
    instagram = models.CharField(verbose_name=_('Instagram'), max_length=100, blank=True, null=True)
    whatsapp = models.CharField(verbose_name=_('WhatsApp'), max_length=100, blank=True, null=True)

    logo = models.CharField(verbose_name=_('Cover'), max_length=100, blank=True, null=True)
    cover = models.CharField(verbose_name=_('Cover'), max_length=100, blank=True, null=True)

    start_work_week_day = models.IntegerField(null=True)
    end_work_week_day = models.IntegerField(null=True)

    default_lang = models.CharField(max_length=20, default=settings.DEFAULT_LANG)
    langs = ArrayField(models.CharField(max_length=20), default=settings.MULTILANDING_LANGS)

    start_work_time_step = models.IntegerField(null=True)
    end_work_time_step = models.IntegerField(null=True)

    sub_domain = models.CharField(verbose_name='Sub domain', db_index=True, unique=True, max_length=50)
    dns_zone_id = models.CharField(verbose_name=_('DNS zone ID'), max_length=150)

    domain = models.ForeignKey(MultilandingDomain, related_name='sub_domains', on_delete=models.PROTECT, null=True)
    
    gallery = ArrayField(models.CharField(max_length=200), blank=True, null=True, size=6)

    class Meta:
        db_table = "multilandings"
        
    @property
    def free_time_slots(self) -> List[Any]:
        slots = []
        for i in range(settings.MAX_TIME_STEPS):
            slots.append({
                'value': i,
                'label': ':'.join(str(timedelta(minutes=i * settings.TIME_STEP_MINUTES)).split(':')[:2])
            })
        return slots

    @property
    def localization(self):
        return {
            'default': self.default_lang,
            'active': self.langs
        }

    @property
    def schedule(self):
        return {
            'days': [self.start_work_week_day, self.end_work_week_day],
            'intervals': [self.start_work_time_step, self.end_work_time_step],
        }

    @property
    def location(self):
        return {
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'building': self.building,
            'gmapApiKey': self.googleMapApiKey
        }

    @property
    def contacts(self):
        return {
            'phone': self.phone,
            'facebook': self.facebook, 
            'instagram': self.instagram,
            'whatsapp': self.whatsapp
        }

    def get_available_langs(self):
        return self.langs

    @property
    def name(self) -> Dict[str, str]:
        return self.get_locale_property(self.NAME)

    @property
    def description(self) -> Dict[str, str]:
        return self.get_locale_property(self.DESCRIPTION)
        
    def __str__(self):
        return f'{self.sub_domain}.{self.domain.domain}'
        
    