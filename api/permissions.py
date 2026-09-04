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

class IsMaterialOwnerOrAdmin(BasePermission):
    """
    Admin:
        - Full access

    Teacher:
        - Only access materials belonging to their teaching assignments

    Student:
        - Read only
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False


class IsMaterialFileOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.material.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.material.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False


class IsFileOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role in {
            "teacher",
            "student",
        }:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        return obj.uploaded_by == request.user

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role in {"teacher", "student"}:
            return obj.uploaded_by == request.user

        return False


class IsAssignmentOwnerOrAdmin(BasePermission):
    """
    Admin:
        - Full access

    Teacher:
        - Only access assignments belonging to their teaching assignments

    Student:
        - Read only
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False


class IsAssignmentFileOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.assignment.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False


class IsSubmissionOwnerOrTeacherOrAdmin(BasePermission):
    """
    Admin:
        - Full access

    Teacher:
        - Access submissions for their own assignments

    Student:
        - Only access their own submissions
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in {
            "admin",
            "teacher",
            "student",
        }

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.assignment.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return (
                obj.student.user
                == request.user
            )

        return False

class IsSubmissionAnswerOwnerOrTeacherOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in {
            "admin",
            "teacher",
            "student",
        }

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.submission.assignment.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return (
                obj.submission.student.user
                == request.user
            )

        return False

class IsSubmissionFileOwnerOrTeacherOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in {
            "admin",
            "teacher",
            "student",
        }

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.submission.assignment
                .teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return (
                obj.submission.student.user
                == request.user
            )

        return False

class IsGradeOwnerOrTeacherOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.assessment.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return (
                request.method in self.SAFE_METHODS
                and obj.student.user == request.user
            )

        return False

class IsAssignmentQuestionOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.assignment.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsAssessmentOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsAssessmentItemOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.assessment.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsGradeComponentOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsReportCardOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role in {"teacher", "student"}:
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return request.method in self.SAFE_METHODS

        if request.user.role == "student":
            return (
                request.method in self.SAFE_METHODS
                and obj.student.user == request.user
            )

        return False

class IsScheduleOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsClassAttendanceSessionOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.schedule.teaching_assignment.teacher.user
                == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsSchoolAttendanceRecordOwnerOrTeacherOrAdmin(
    BasePermission
):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in {
            "admin",
            "teacher",
            "student",
        }

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return (
                request.method in self.SAFE_METHODS
                and obj.student.user == request.user
            )

        return False

class IsSchoolAttendanceSessionOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role in {"admin", "teacher"}:
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role in {"admin", "teacher"}:
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsAnnouncementOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return True

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role == "teacher":
            return (
                obj.created_by == request.user
            )

        if request.user.role == "student":
            return request.method in self.SAFE_METHODS

        return False

class IsNotificationOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role in {
            "teacher",
            "student",
        }:
            return request.method in self.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if request.user.role in {
            "teacher",
            "student",
        }:
            return (
                obj.user == request.user
            )

        return False

class IsConversationMemberOrOwnerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role in {
            "teacher",
            "student",
        }:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if obj.created_by == request.user:
            return True

        if request.method in self.SAFE_METHODS:
            return obj.members.filter(
                user=request.user
            ).exists()

        return False

class IsConversationMemberManagerOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role in {
            "teacher",
            "student",
        }:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        if obj.conversation.created_by == request.user:
            return True

        if request.method in self.SAFE_METHODS:
            return obj.user == request.user

        return False

class IsMessageMemberOrAdmin(BasePermission):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "admin":
            return True

        if request.user.role in {
            "teacher",
            "student",
        }:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        is_member = obj.conversation.members.filter(
            user=request.user
        ).exists()

        if not is_member:
            return False

        if request.method in self.SAFE_METHODS:
            return True

        return False

