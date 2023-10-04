from typing import Any, List

from rest_framework.serializers import *  # noqa

from django.conf import settings

from apps.locales.models import MultilandingLocale
from randevu.models import ModelWithLocales


class Validator(Serializer):  # noqa
    """Validator is a DRF-serializer based validator for end-user data
    Use it to produce developer-friendly errors
    """
    @classmethod
    def do(cls, data: dict, context: dict[str, Any]) -> bool:
        instance = cls(data=data, context=context)

        return instance.is_valid(raise_exception=True)


def create_serializer_class(name, fields):
    return type(name, (Validator, ), fields)


def inline_validator(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


class LocaleValidator(Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for lang in settings.MULTILANDING_LANGS:
            self.fields[lang] = CharField(required=False)


class BasePropertyLocaleValidator():
    localized_fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.localized_fields:
            self.fields[field[0]] = LocaleValidator(required=False)

    def validate(self, data) -> Any:
        data = super().validate(data)
        data['locales'] = self._extract_localized_properites(data)
        return data

    def create(self, validated_data: Any):
        locales = validated_data.pop('locales', None)
        obj = super().create(validated_data)
        if not isinstance(obj, ModelWithLocales):
            raise Exception('Instance should be inherited from ModelWithLocales model.')
        obj.set_locales(locales)
        return obj

    def update(self, instance: Any, validated_data: Any) -> Any:
        """Find difference in both locales list and apply one to another."""

        if not isinstance(instance, ModelWithLocales):
            raise Exception('Instance should be inherited from ModelWithLocales model.')
            
        self._update_locales(instance, validated_data.pop('locales', None))
        return super().update(instance, validated_data)

    def _extract_localized_properites(self, data) -> List[MultilandingLocale]:
        localized_fields = [ l[0] for l in self.localized_fields ]

        locales = []
        for item in localized_fields:
            value = data.pop(item, None)
            if value:
                for lang, translation in value.items():
                    locales.append(MultilandingLocale(lang=lang, text=translation, alias=item))
        return locales

    def _update_locales(self, instance, body_locales) -> List[MultilandingLocale]:
        db_locales = instance.locales.all()
        does_update_locales = len(db_locales) != len(body_locales) \
            or len(set(list(db_locales)).symmetric_difference(set(body_locales))) > 0
       
        if does_update_locales:
            db_locales.delete()
            return instance.set_locales(body_locales)

        return body_locales


class ModelValidatorWithLocalization(BasePropertyLocaleValidator, ModelSerializer):
    pass


class ValidatorWithLocalization(BasePropertyLocaleValidator, Validator):
    pass


class PaginationSerializer(Serializer):
    page = IntegerField()
    count = IntegerField()