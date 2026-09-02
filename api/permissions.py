from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):
    """
    Allow access only to users with the admin role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsTeacherUserRole(BasePermission):
    """
    Allow access only to users with the teacher role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "teacher"
        )


class IsStudentUserRole(BasePermission):
    """
    Allow access only to users with the student role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "student"
        )


class IsAdminOrTeacherRole(BasePermission):
    """
    Allow access to admin or teacher users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["admin", "teacher"]
        )


class IsAdminOrTeacherOrStudentRole(BasePermission):
    """
    Allow access to any authenticated application user.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in [
                "admin",
                "teacher",
                "student",
            ]
        )