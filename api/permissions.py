from rest_framework.permissions import BasePermission


# ============================================================
# ROLE PERMISSIONS
# ============================================================

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
            and request.user.role in {
                "admin",
                "teacher",
            }
        )


class IsAuthenticatedApplicationUser(BasePermission):
    """
    Allow access to authenticated application users.

    Application roles:
    - admin
    - teacher
    - student
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in {
                "admin",
                "teacher",
                "student",
            }
        )


# ============================================================
# SAFE READ / WRITE
# ============================================================

class IsAdminOrReadOnly(BasePermission):
    """
    Admin can perform all actions.

    Other authenticated users can only read.
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        return request.method in self.SAFE_METHODS


class IsAdminOrTeacherWriteReadOnly(BasePermission):
    """
    Admin and teacher can write.

    Student can only read.
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role in {
            "admin",
            "teacher",
        }:
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False


# ============================================================
# OWNERSHIP
# ============================================================

class IsTeacherOwnerOrAdmin(BasePermission):
    """
    Allow access to admin or the teacher who owns the object.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        teacher_profile = getattr(
            obj,
            "teacher",
            None,
        )

        if teacher_profile is not None:
            return teacher_profile.user == request.user

        teaching_assignment = getattr(
            obj,
            "teaching_assignment",
            None,
        )

        if teaching_assignment is not None:
            return (
                teaching_assignment.teacher.user
                == request.user
            )

        return False


class IsStudentOwnerOrAdmin(BasePermission):
    """
    Allow access to admin or the student who owns the object.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        student_profile = getattr(
            obj,
            "student",
            None,
        )

        if student_profile is not None:
            return student_profile.user == request.user

        return False