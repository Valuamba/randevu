from typing import List, Any, Type
from ast import operator
import uuid

from django.db import models
from django.apps import apps
from django.utils.functional import cached_property

from functools import reduce
import inflection


class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelWithLocales(TimeStampedUUIDModel):
    def get_available_langs(self):
        return self.company.langs

    def set_locales(self, locales):
        ''' We check current multilanding langs and locales that goes to be added in DB.
        '''
        langs = self.get_available_langs()
        class_name = inflection.underscore(self.__class__.__name__)
        multilanding_type = apps.get_model('locales.MultilandingLocale')

        if not hasattr(multilanding_type, class_name):
            raise Exception(f'Multilanding Locale doesn\'t contain field {class_name}.')

        for locale in locales:
            if locale.lang in langs:
                setattr(locale, class_name, self)
            else:
                raise Exception(f'Current multilanding doesn\'t allow lang {locale.lang}')

        multilanding_type.objects.bulk_create(locales)
        return locales

    @cached_property
    def get_locales(self) -> List[Any]:
        return self.locales.all()

    def get_locale_property(self, prop: str):
        return { l.lang:l.text for l in self.get_locales if l.alias == prop }

    @property
    def locales(self):
        return self.locales.all()

    class Meta:
        abstract = True