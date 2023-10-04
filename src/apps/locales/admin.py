from django.contrib import admin

from apps.locales.models import MultilandingLocale
# Register your models here.


class LocalesAdmin(admin.ModelAdmin):
    list_display = ('pkid', 'id', 'lang', 'alias', 'text', 'category', 'salon_service', 'multilanding', 'created_at', 'update_at')
    
    
admin.site.register(MultilandingLocale, LocalesAdmin)