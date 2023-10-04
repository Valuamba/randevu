from django.contrib import admin

from apps.mailing.models import EmailConfiguration


class EmailConfigurationAdmin(admin.ModelAdmin):

    fields = [
        'backend',
        'from_email',
        'backend_options',
    ]


admin.site.register(EmailConfiguration, EmailConfigurationAdmin)