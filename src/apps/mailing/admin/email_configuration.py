from randevu.admin import StackedInline
from django.contrib import admin

from apps.mailing.models import EmailConfiguration


class EmailConfigurationAdmin(admin.ModelAdmin):
    model = EmailConfiguration

    fields = [
        'backend',
        'from_email',
        'backend_options',
    ]


admin.site.register(EmailConfigurationAdmin)