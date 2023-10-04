from django.contrib import admin

from apps.schedule.models import StaffSchedule, StaffBreak


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['pkid', 'id', 'week_day', 'start_work_time_step', 'end_work_time_step', 'is_day_off',
        'user', 'created_at', 'update_at'    
    ]


class BreakAdmin(admin.ModelAdmin):
    list_display = [
        'pkid', 'id', 'start_break_time_step', 'end_break_time_step', 'schedule', 'created_at', 'update_at' 
    ]


admin.site.register(StaffSchedule, ScheduleAdmin)
admin.site.register(StaffBreak, BreakAdmin)