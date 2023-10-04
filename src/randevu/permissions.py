from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

from apps.users.models import User


class BaseUserPermissions(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_active == True and user.status != User.REMOVED

class OwnerOnly(BaseUserPermissions):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_owner and user.role == User.OWNER \
            and super().has_permission(request, view)

class AdminOnly(BaseUserPermissions):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and super().has_permission(request, view) and \
             (user.role == User.ADMIN or (user.is_owner and user.role == User.OWNER))

class EmployeeOnly(BaseUserPermissions):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and super().has_permission(request, view) and \
            (user.role == User.ADMIN or \
                (user.is_owner and user.role == User.OWNER) or \
                (user.role == User.EMPLOYEE)
            )


__all__ = [
    'AllowAny',
    'IsAuthenticated',
    'SuperUserOnly',
    'OwnerOnly',
    'AdminOnly',
    'EmployeeOnly'
]
