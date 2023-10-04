from django.contrib import admin

from apps.service.models import SalonService, Category


class SerivceAdmin(admin.ModelAdmin):
    list_display = ('pkid', 'id', 'duration', 'gender', 'price', 'image', 'category' , 
        'company', 'is_deleted', 'created_at', 'update_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pkid', 'id', 'image', 'company', 'is_deleted', 'created_at', 'update_at'
    )
    
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(SalonService, SerivceAdmin)