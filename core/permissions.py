from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(request.user and request.user.is_staff)


class IsWaiter(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(
            request.user and
            request.user.groups.filter(name='Waiter').exists()
        )


class IsKitchenStaff(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(
            request.user and
            request.user.groups.filter(name='Kitchen').exists()
        )


class IsAdminOrWaiter(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        if not request.user:
            return False
        return bool(
            request.user.is_staff or
            request.user.groups.filter(name='Waiter').exists()
        )


class IsAdminOrKitchen(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        if not request.user:
            return False
        return bool(
            request.user.is_staff or
            request.user.groups.filter(name='Kitchen').exists()
        )