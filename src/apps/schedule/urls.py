from django.urls import path

from apps.schedule.api.views import StaffScheduleAPIView


urlpatterns = [
    path('schedule/<str:employee_id>/update', StaffScheduleAPIView.as_view(), name='schedule')
]
