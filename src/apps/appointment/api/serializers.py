
from typing import Any
from rest_framework import serializers

from apps.appointment.models import Appointment
from apps.client.api.serializers import CreateClientSerializer
from randevu.validators import inline_validator

from phonenumber_field.serializerfields import PhoneNumberField

from apps.employee.api.serializers import EmployeeSerialzer
from apps.service.api.serializers import CategorySerializer, SalonServiceSerializer
from apps.client.api.serializers import ClientSerializer

from randevu.validators import inline_validator


class AppointmentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerialzer()
    client = ClientSerializer()
    service = SalonServiceSerializer()
    category = CategorySerializer()
    date = inline_validator(fields={
        'day': serializers.DateField(),
        'time_step': serializers.IntegerField()
    }, read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'pkid',
            'id',
            'index',
            'status',
            'employee',
            'category',
            'service',
            'client',
            'date',
        ]


class CreateAppointmentSerializer(serializers.Serializer):
    client = inline_validator(fields={
        'name': serializers.CharField(),
        'phone': PhoneNumberField()
    })
    employee = inline_validator(fields={
        'id': serializers.IntegerField()
    })
    service = inline_validator(fields={
        'id': serializers.IntegerField()
    })
    date = inline_validator(fields={
        'day': serializers.DateField(),
        'time_step': serializers.IntegerField()
    })
    category = inline_validator(fields={
        'id': serializers.IntegerField()
    })


class AppointmentFilterSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    count = serializers.IntegerField()


class AppointmentParametersSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text="Appointment status.")
    interval = serializers.IntegerField(help_text="Appointment creation interval.")
    client_pkid = serializers.IntegerField(help_text='Appointment client pkid.')