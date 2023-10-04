from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint, Q

from apps.multilanding.models import Multilanding
from apps.service.models import Category, SalonService
from apps.common.models import TimeStampedUUIDModel


def allow_only_one_entity():
    unique_entity_query = Q(multilanding__isnull=True, salon_service__isnull=False, category__isnull=True) | \
        Q(multilanding__isnull=True, salon_service__isnull=True, category__isnull=False) | \
        Q(multilanding__isnull=False, salon_service__isnull=True, category__isnull=True)

    return unique_entity_query


class MultilandingLocale(TimeStampedUUIDModel):
    lang = models.CharField(verbose_name=_('Lang'), max_length=2)
    alias = models.CharField(verbose_name=_('Alias'), max_length=100)
    text = models.CharField(verbose_name=_('Text'), max_length=100)

    multilanding = models.ForeignKey(Multilanding, related_name='locales', null=True, blank=True, on_delete=models.PROTECT)
    salon_service      = models.ForeignKey(SalonService, related_name='locales', null=True, blank=True, on_delete=models.PROTECT)
    category     = models.ForeignKey(Category,     related_name='locales', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'multilanding.locales'
        verbose_name = _('Multilanding Locale')
        verbose_name_plural = _('Multilanding Locales')

        constraints = [
            models.UniqueConstraint(fields=['multilanding', 'lang', 'alias'], name='unque_multilanding_lang'),
            models.UniqueConstraint(fields=['salon_service', 'lang', 'alias'], name='unque_salon_service_lang'),
            models.UniqueConstraint(fields=['category', 'lang', 'alias'], name='unque_category_lang'),

            CheckConstraint(check=allow_only_one_entity(), name='check_valid_locale_entity')
        ]

        indexes = [
            models.Index(fields=['lang', 'alias'])
        ]

    def get_locale_type_name(self) -> str:
        if self.multilanding:
            return 'multilanding'
        elif self.service:
            return 'service'
        elif self.category:
            return 'category'
        
        
    def __hash__(self) -> int:
        return hash((self.lang, self.alias, self.text))

    def __eq__(self, other):
        return self.lang, self.alias, self.text == other.lang,other.alias, self.text

    def __ne__(self, other):
        return not self.__eq__(other)