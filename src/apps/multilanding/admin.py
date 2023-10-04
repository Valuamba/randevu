from django.contrib import admin

from apps.multilanding.models import MultilandingDomain, Multilanding


class MultilandingDomainAdmin(admin.ModelAdmin):
    list_display = ('pkid', 'id', 'domain', 'created_at', 'update_at')


class MultilandingAdmin(admin.ModelAdmin):
    list_display = (
        'pkid', 'id', 'sub_domain', 'country', 'city', 'street', 'building',
        'googleMapApiKey', 'phone', 'facebook', 'instagram', 'whatsapp', 'cover',
        'start_work_week_day', 'end_work_week_day', 'dns_zone_id', 'domain', 
        'gallery',  'created_at', 'update_at'
    )
    
    
admin.site.register(MultilandingDomain, MultilandingDomainAdmin)
admin.site.register(Multilanding, MultilandingAdmin)
