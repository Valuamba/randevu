from django.contrib import admin

from apps.appointment.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pkid', 'id', 'employee', 'category', 'service', 'client', 'time_step',
        'day', 'status', 'company', 'is_deleted', 'created_at', 'update_at')


admin.site.register(Appointment, AppointmentAdmin)