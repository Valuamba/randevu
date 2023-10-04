from rest_framework import serializers

from django.apps import apps

from apps.service.models import Category, SalonService

from randevu.validators import inline_validator


from randevu.validators import ModelValidatorWithLocalization


class SalonServiceSerializer(ModelValidatorWithLocalization):
    pkid = serializers.IntegerField(read_only=True)
    localized_fields = Category.LOCALIZED_FIELDS
    employees = inline_validator(fields={
        'pkid': serializers.IntegerField(),
        'name': serializers.CharField(),
        'image': serializers.CharField()
    }, many=True)
    

    class Meta:
        model = SalonService
        fields = [
            'pkid',
            'id',
            'category',
            'duration',
            'gender',
            'employees',
            'price',
            'image'
        ]


class SalonServiceCreateSerializer(ModelValidatorWithLocalization):
    pkid = serializers.IntegerField(read_only=True)
    localized_fields = Category.LOCALIZED_FIELDS

    category = inline_validator(fields={
        'pkid': serializers.IntegerField()
    })

    class Meta:
        model = SalonService
        fields = [
            'pkid',
            'category',
            'duration',
            'gender',
            'price',
            'image',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        category = validated_data.pop('category')
        locales = validated_data.pop('locales', None)

        validated_data['category_id'] = category['pkid']

        service = SalonService.objects.create(**validated_data, company=user.company)
        service.set_locales(locales)
        return service

    def update(self, instance, validated_data):
        self._update_locales(instance, validated_data.pop('locales', None))
        category = validated_data.pop('category')

        instance.category_id = category['pkid']
        instance.duration = validated_data['duration']
        instance.gender = validated_data['gender']
        instance.price = validated_data['price']
        instance.image = validated_data['image']

        instance.save()

        return instance


class CategorySerializer(ModelValidatorWithLocalization):
    localized_fields = Category.LOCALIZED_FIELDS
    services = SalonServiceSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'pkid',
            'id',
            'image',
            'services'
        ]

class CategoryCreateSerializer(ModelValidatorWithLocalization):
    localized_fields = Category.LOCALIZED_FIELDS

    class Meta:
        model = Category
        fields = [
            'pkid',
            'image'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['company'] = user.company
        
        return super().create(validated_data)