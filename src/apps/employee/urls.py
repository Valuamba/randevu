from django.urls import include, path

from apps.employee.api.views import CalculateFreeEmployeeTimeSlotsAPIView
from apps.employee.api.viewsets import EmployeeViewSet


open_urls = [
    path('open/employees/', EmployeeViewSet.as_view({'get': 'list'})),
    path('open/times/', CalculateFreeEmployeeTimeSlotsAPIView.as_view())
]


urlpatterns = [
    path('employee/times/', CalculateFreeEmployeeTimeSlotsAPIView.as_view(), name='calculate-free-slots'),
    path('employee/create/', EmployeeViewSet.as_view({'post': 'create'})),
    path('employee/<str:pkid>/update/', EmployeeViewSet.as_view({'put': 'update'})),
    path('employee/<str:pkid>/delete/', EmployeeViewSet.as_view({'delete': 'destroy'})),
    path('employee/<str:pkid>/', EmployeeViewSet.as_view({'get': 'retrieve'})),

    path('employees/', EmployeeViewSet.as_view({'get': 'list'}))

] + open_urls