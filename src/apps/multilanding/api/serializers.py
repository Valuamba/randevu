
from rest_framework import serializers
from rest_framework import serializers

from django.conf import settings

from randevu.validators import ModelValidatorWithLocalization, Validator, ValidatorWithLocalization
from randevu import validators

from apps.multilanding.models import Multilanding
from apps.multilanding.models import Multilanding
from apps.multilanding.services import SubDomainUpdater

from phonenumber_field.serializerfields import PhoneNumberField


class CompanyInfoSerializer(serializers.Serializer):
    pkid = serializers.IntegerField()
    name = serializers.CharField(allow_blank=True, allow_null=True)
    logo = serializers.CharField(allow_blank=True, allow_null=True)
    subdomain = serializers.CharField()


class CompanySerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, allow_null=True)
    logo = serializers.CharField(allow_blank=True, allow_null=True)


#Multilanding


class MultilandingLocationValidator(Validator):
    country = validators.CharField(required=False)
    city = validators.CharField(required=False)
    street = validators.CharField(required=False)
    building = validators.CharField(required=False)
    gmapApiKey = serializers.CharField(required=False)


class MultilandingSchedueleValidator(Validator):
    days = validators.ListField(child=validators.IntegerField(), required=False)
    intervals = validators.ListField(child=validators.IntegerField(), required=False)


class MultilandingContactsValidator(Validator):
    phone = PhoneNumberField(required=False)
    facebook = validators.CharField(required=False)
    instagram = validators.CharField(required=False)
    whatsapp = validators.CharField(required=False)


class MultilandingSerializer(ModelValidatorWithLocalization):
    localized_fields = Multilanding.LOCALIZED_FIELDS

    location = MultilandingLocationValidator(required=False)
    schedule = MultilandingSchedueleValidator(required=False)
    contacts = MultilandingContactsValidator(required=False)

    cover = validators.CharField(required=False)
    logo = validators.CharField(required=False)
    gallery = validators.ListField(child=validators.CharField(), required=False)

    class Meta:
        model = Multilanding
        fields = [
            'contacts',
            'location',
            'schedule',
            'cover',
            'logo',
            'gallery'
        ]


class UpdateMultilandingSerializer(ModelValidatorWithLocalization):
    localized_fields = Multilanding.LOCALIZED_FIELDS

    location = MultilandingLocationValidator(required=False)
    schedule = MultilandingSchedueleValidator(required=False)
    contacts = MultilandingContactsValidator(required=False)

    # cover = validators.CharField(required=False)
    # gallery = validators.ListField(child=validators.CharField(), required=False)

    class Meta:
        model = Multilanding
        fields = [
            'contacts',
            'location',
            'schedule',
            'logo',
            'cover',
            'gallery'
        ]

    def update(self, instance, validated_data):
        for k, v in validated_data.pop('contacts').items():
            validated_data[k] = v

        for k, v in validated_data.pop('location').items():
            validated_data[k] = v

        schedule = validated_data.pop('schedule', None)
        if schedule:
            validated_data['start_work_week_day'] = schedule['days'][0]
            validated_data['end_work_week_day'] = schedule['days'][1]

            validated_data['start_work_time_step'] = schedule['intervals'][0]
            validated_data['end_work_time_step'] = schedule['intervals'][1]

        return super().update(instance, validated_data)


class MultilandingLocalization(validators.Validator):
    default = serializers.CharField()
    active = serializers.ListField(child=serializers.CharField())


class TimeSlotSerializer(validators.Validator):
    value = validators.IntegerField()
    label = validators.CharField()


class SettingsSerializer(validators.ModelSerializer):
    localization = MultilandingLocalization()
    free_time_slots = validators.ListField(child=TimeSlotSerializer(), read_only=True)
    sub_domain = validators.CharField()

    class Meta:
        model = Multilanding
        fields = [
            'localization',
            'free_time_slots',
            'sub_domain'
        ]

    def update(self, instance, validated_data):
        localization = validated_data.pop('localization')
        default_lang = localization['default']
        langs = localization['active']
        user = self.context['request'].user

        if default_lang not in langs:
            raise validators.ValidationError('Default lang doesn\'t exist in available langs.')

        if len(set(langs) - set(settings.MULTILANDING_LANGS)) > 0:
            raise validators.ValidationError('Default langs does not match valid languages.')

        validated_data['default_lang'] = default_lang
        validated_data['langs'] = langs

        if validated_data['sub_domain'] != instance.sub_domain:
            SubDomainUpdater(validated_data['sub_domain'], user, instance.dns_zone_id)()
        return super().update(instance, validated_data)
