
from randevu.permissions import OwnerOnly


class MultilandingPermissions(OwnerOnly):
    def has_permission(self, request, view) -> bool:
        if view.action in ['retrieve', 'company', 'info']:
            return True
        return super().has_permission(request, view)