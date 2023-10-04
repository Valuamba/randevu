
from rest_framework import permissions

from randevu.permissions import AdminOnly, OwnerOnly, EmployeeOnly


class ClientPermissions(EmployeeOnly):
    def has_permission(self, request, view) -> bool:
        return super().has_permission(request, view)
