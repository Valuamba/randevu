
from rest_framework import permissions

from randevu.permissions import AdminOnly, OwnerOnly, EmployeeOnly


class ServicePermissions(EmployeeOnly):
    def has_permission(self, request, view) -> bool:
        if view.action == 'list':
            return True
        return super().has_permission(request, view)



class CategoryPermissions(EmployeeOnly):
    def has_permission(self, request, view) -> bool:
        if view.action == 'list':
            return True
        return super().has_permission(request, view)