from django.contrib import admin

from apps.client.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('pkid', 'id', 'name', 'phone', 'email', 'whatsapp', 'notes',
        'is_deleted', 'company', 'is_deleted', 'created_at', 'update_at')


admin.site.register(Client, ClientAdmin)