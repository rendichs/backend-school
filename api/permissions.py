from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):
    """
    Hanya user dengan role 'admin'
    yang dapat mengakses endpoint ini.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )