from apps.client.models import Client

from rest_framework import serializers 

from randevu.validators import inline_validator
from randevu import validators


class ClientAppointmentsStatisticSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_price = serializers.IntegerField()


class ClientContactSerializer(validators.Validator):
    phone = validators.CharField()
    email = validators.EmailField()
    whatsapp = validators.BooleanField()


class ClientSerializer(serializers.ModelSerializer):
    appointments_statistic = ClientAppointmentsStatisticSerializer(read_only=True)
    contacts = ClientContactSerializer()
    
    class Meta:
        model = Client
        fields = [
            'pkid',
            'id',
            'name',
            'phone',
            'notes',
            'contacts',
            'appointments_statistic'
        ]


class CreateClientSerializer(serializers.ModelSerializer):
    contacts = ClientContactSerializer()

    class Meta:
        model = Client
        fields = [ 
            'name',
            'notes',
            'contacts'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        contacts = validated_data.pop('contacts')
        for k, v in contacts.items():
            validated_data[k] = v
        validated_data['company'] = user.company
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        contacts = validated_data.pop('contacts')
        for k, v in contacts.items():
            validated_data[k] = v
        validated_data['company'] = user.company
        return super().update(instance, validated_data)