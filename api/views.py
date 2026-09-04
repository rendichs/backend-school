from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.decorators import action
from django.db.models import Q

from .permissions import (
    IsAdminUserRole,
    IsTeacherUserRole,
    IsStudentUserRole,
    IsAdminOrTeacherRole,
    IsAuthenticatedApplicationUser,
    IsAdminOrReadOnly,
    IsAdminOrTeacherWriteReadOnly,
    IsTeacherOwnerOrAdmin,
    IsStudentOwnerOrAdmin,
    IsMaterialOwnerOrAdmin,
    IsMaterialFileOwnerOrAdmin,
    IsFileOwnerOrAdmin,
    IsAssignmentOwnerOrAdmin,
    IsAssignmentFileOwnerOrAdmin,
    IsSubmissionOwnerOrTeacherOrAdmin,
    IsSubmissionAnswerOwnerOrTeacherOrAdmin,
    IsSubmissionFileOwnerOrTeacherOrAdmin,
    IsGradeOwnerOrTeacherOrAdmin,
    IsAssignmentQuestionOwnerOrAdmin,
    IsAssessmentOwnerOrAdmin,
    IsAssessmentItemOwnerOrAdmin,
    IsGradeComponentOwnerOrAdmin,
    IsReportCardOwnerOrAdmin,
    IsScheduleOwnerOrAdmin,
    IsClassAttendanceSessionOwnerOrAdmin,
    IsClassAttendanceRecordOwnerOrTeacherOrAdmin,
    IsSchoolAttendanceSessionAdminOrTeacher,
    IsSchoolAttendanceSessionOwnerOrAdmin,
    IsSchoolAttendanceRecordOwnerOrTeacherOrAdmin,
    IsNotificationOwnerOrAdmin,
    IsAnnouncementOwnerOrAdmin,
    IsConversationMemberOrOwnerOrAdmin,
    IsConversationMemberManagerOrAdmin,
    IsMessageMemberOrAdmin,
    IsSettingAdminOrReadOnly,
    IsAdminActivityLog,
    IsAdminAuditLog,
)

from .models import (
    CustomUser,
    School,
    TeacherProfile,
    StudentProfile,
    AcademicYear,
    Semester,
    Program,
    InterestClass,
    SchoolClass,
    ClassMember,
    SubjectGroup,
    Subject,
    TeachingAssignment,
    File,
    Material,
    MaterialFile,
    Assignment,
    AssignmentFile,
    AssignmentQuestion,
    AssignmentSubmission,
    SubmissionAnswer,
    SubmissionFile,
    Assessment,
    AssessmentItem,
    Grade,
    GradeComponent,
    ReportCard,
    Schedule,
    SchoolAttendanceSession,
    SchoolAttendanceRecord,
    ClassAttendanceSession,
    ClassAttendanceRecord,
    Announcement,
    Notification,
    Conversation,
    ConversationMember,
    Message,
    Setting,
    ActivityLog,
    AuditLog,
)

from .serializers import (
    UserSerializer,
    SchoolSerializer,
    TeacherSerializer,
    StudentSerializer,
    AcademicYearSerializer,
    SemesterSerializer,
    ProgramSerializer,
    InterestClassSerializer,
    SchoolClassSerializer,
    ClassMemberSerializer,
    SubjectGroupSerializer,
    SubjectSerializer,
    TeachingAssignmentSerializer,
    FileSerializer,
    MaterialSerializer,
    MaterialFileSerializer,
    AssignmentSerializer,
    AssignmentFileSerializer,
    AssignmentQuestionSerializer,
    AssignmentSubmissionSerializer,
    SubmissionAnswerSerializer,
    SubmissionFileSerializer,
    AssessmentSerializer,
    AssessmentItemSerializer,
    GradeSerializer,
    GradeComponentSerializer,
    ReportCardSerializer,
    ScheduleSerializer,
    SchoolAttendanceSessionSerializer,
    SchoolAttendanceRecordSerializer,
    ClassAttendanceSessionSerializer,
    ClassAttendanceRecordSerializer,
    AnnouncementSerializer,
    NotificationSerializer,
    ConversationSerializer,
    ConversationMemberSerializer,
    MessageSerializer,
    SettingSerializer,
    ActivityLogSerializer,
    AuditLogSerializer,
    CustomAuthTokenSerializer,
)

from .permissions import IsAdminUserRole


# ============================================================
# USER
# ============================================================

class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated
    ]


# ============================================================
# SCHOOL
# ============================================================

class SchoolViewSet(viewsets.ModelViewSet):

    queryset = School.objects.all()

    serializer_class = SchoolSerializer

    permission_classes = [
        IsAdminUserRole
    ]

    def destroy(self, request, *args, **kwargs):
        return Response(
            {
                "detail": "School cannot be deleted."
            },
            status=status.HTTP_403_FORBIDDEN,
        )


# ============================================================
# TEACHER
# ============================================================

class TeacherViewSet(viewsets.ModelViewSet):

    queryset = (
        CustomUser.objects
        .filter(role="teacher")
        .select_related("teacher_profile")
    )

    serializer_class = TeacherSerializer

    permission_classes = [
        IsAdminUserRole
    ]

    def destroy(self, request, *args, **kwargs):

        teacher = self.get_object()

        profile = getattr(
            teacher,
            "teacher_profile",
            None
        )

        if profile:

            dependencies = {}

            teaching_assignments = (
                TeachingAssignment.objects
                .filter(teacher=profile)
                .count()
            )

            if teaching_assignments > 0:
                dependencies["teaching_assignments"] = (
                    teaching_assignments
                )

            if dependencies:

                return Response(
                    {
                        "detail": (
                            f"Teacher {teacher.full_name} "
                            "cannot be deleted because "
                            "the teacher is still being used."
                        ),
                        "code": "teacher_in_use",
                        "dependencies": dependencies,
                    },
                    status=status.HTTP_409_CONFLICT,
                )

        return super().destroy(
            request,
            *args,
            **kwargs
        )


# ============================================================
# STUDENT
# ============================================================

class StudentViewSet(viewsets.ModelViewSet):

    queryset = (
        CustomUser.objects
        .filter(role="student")
        .select_related("student_profile")
    )

    serializer_class = StudentSerializer

    permission_classes = [
        IsAdminUserRole
    ]


# ============================================================
# ACADEMIC
# ============================================================

class AcademicYearViewSet(viewsets.ModelViewSet):

    queryset = AcademicYear.objects.all()

    serializer_class = AcademicYearSerializer

    permission_classes = [
        IsAdminUserRole
    ]


class SemesterViewSet(viewsets.ModelViewSet):

    queryset = Semester.objects.all()

    serializer_class = SemesterSerializer

    permission_classes = [
        IsAdminUserRole
    ]


class ProgramViewSet(viewsets.ModelViewSet):

    queryset = Program.objects.all()

    serializer_class = ProgramSerializer

    permission_classes = [
        IsAdminUserRole
    ]


class InterestClassViewSet(viewsets.ModelViewSet):

    queryset = InterestClass.objects.all()

    serializer_class = InterestClassSerializer

    permission_classes = [
        IsAdminUserRole
    ]


class SchoolClassViewSet(viewsets.ModelViewSet):

    queryset = SchoolClass.objects.all()

    serializer_class = SchoolClassSerializer

    permission_classes = [
        IsAdminUserRole
    ]


class ClassMemberViewSet(viewsets.ModelViewSet):

    queryset = ClassMember.objects.all()

    serializer_class = ClassMemberSerializer

    permission_classes = [
        IsAdminUserRole
    ]


# ============================================================
# SUBJECT
# ============================================================

class SubjectGroupViewSet(viewsets.ModelViewSet):

    queryset = SubjectGroup.objects.all()

    serializer_class = SubjectGroupSerializer

    permission_classes = [
        IsAdminUserRole
    ]


class SubjectViewSet(viewsets.ModelViewSet):

    queryset = Subject.objects.all()

    serializer_class = SubjectSerializer

    permission_classes = [
        IsAdminUserRole
    ]


# ============================================================
# TEACHING ASSIGNMENT
# ============================================================

class TeachingAssignmentViewSet(viewsets.ModelViewSet):

    queryset = TeachingAssignment.objects.select_related(
        "teacher",
        "subject",
        "school_class",
        "academic_year",
        "semester",
    )

    serializer_class = TeachingAssignmentSerializer

    permission_classes = [
        IsAdminUserRole
    ]


# ============================================================
# FILE
# ============================================================

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.select_related(
        "uploaded_by",
    )
    serializer_class = FileSerializer
    permission_classes = [
        IsFileOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role != "admin":
            queryset = queryset.filter(
                uploaded_by=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            uploaded_by=self.request.user
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            serializer.save()
            return

        if serializer.instance.uploaded_by != self.request.user:
            raise PermissionDenied(
                "You can only manage your own files."
            )

        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if instance.uploaded_by != self.request.user:
            raise PermissionDenied(
                "You can only delete your own files."
            )

        instance.delete()


class MaterialFileViewSet(viewsets.ModelViewSet):
    queryset = MaterialFile.objects.select_related(
        "material",
        "material__teaching_assignment",
        "material__teaching_assignment__teacher",
        "file",
        "file__uploaded_by",
    )
    serializer_class = MaterialFileSerializer
    permission_classes = [
        IsMaterialFileOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                material__teaching_assignment__teacher__user=
                self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        material = serializer.validated_data["material"]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":
            if (
                material.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only attach files to your own materials."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "Students cannot create material files."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":
            if (
                instance.material.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage files of your own materials."
                )

            new_material = serializer.validated_data.get(
                "material",
                instance.material,
            )

            if (
                new_material.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move files to your own materials."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "Students cannot modify material files."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if self.request.user.role == "teacher":
            if (
                instance.material.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only delete files of your own materials."
                )

            instance.delete()
            return

        raise PermissionDenied(
            "Students cannot delete material files."
        )


class AssignmentFileViewSet(viewsets.ModelViewSet):
    queryset = AssignmentFile.objects.select_related(
        "assignment",
        "assignment__teaching_assignment",
        "assignment__teaching_assignment__teacher",
        "file",
        "file__uploaded_by",
    )
    serializer_class = AssignmentFileSerializer
    permission_classes = [
        IsAssignmentFileOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                assignment__teaching_assignment__teacher__user=
                self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        assignment = serializer.validated_data["assignment"]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":
            if (
                assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only attach files to your own assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "Students cannot create assignment files."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":
            if (
                instance.assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage files of your own assignments."
                )

            new_assignment = serializer.validated_data.get(
                "assignment",
                instance.assignment,
            )

            if (
                new_assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move files to your own assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "Students cannot modify assignment files."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if self.request.user.role == "teacher":
            if (
                instance.assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only delete files of your own assignments."
                )

            instance.delete()
            return

        raise PermissionDenied(
            "Students cannot delete assignment files."
        )


class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.select_related(
        "submission",
        "submission__assignment",
        "submission__assignment__teaching_assignment",
        "submission__assignment__teaching_assignment__teacher",
        "submission__student",
        "submission__student__user",
        "file",
        "file__uploaded_by",
    )
    serializer_class = SubmissionFileSerializer
    permission_classes = [
        IsSubmissionFileOwnerOrTeacherOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                submission__assignment
                __teaching_assignment
                __teacher__user=self.request.user
            )

        elif self.request.user.role == "student":
            queryset = queryset.filter(
                submission__student__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        submission = serializer.validated_data["submission"]

        if self.request.user.role == "admin":
            serializer.save(
                file__uploaded_by=self.request.user
            )
            return

        if self.request.user.role == "teacher":
            if (
                submission.assignment
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage files of submissions "
                    "for your own assignments."
                )

            serializer.save()
            return

        if self.request.user.role == "student":
            if (
                submission.student.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only upload files to your own submission."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create a submission file."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":
            if (
                instance.submission.assignment
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage files of your own assignments."
                )

            serializer.save()
            return

        if self.request.user.role == "student":
            if (
                instance.submission.student.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage your own submission files."
                )

            new_submission = serializer.validated_data.get(
                "submission",
                instance.submission,
            )

            if (
                new_submission.student.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move files to your own submission."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update this submission file."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if self.request.user.role == "teacher":
            if (
                instance.submission.assignment
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only delete files of your own assignments."
                )

            instance.delete()
            return

        if self.request.user.role == "student":
            if (
                instance.submission.student.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only delete your own submission files."
                )

            instance.delete()
            return

        raise PermissionDenied(
            "You do not have permission to delete this submission file."
        )


# ============================================================
# MATERIAL
# ============================================================

class MaterialViewSet(viewsets.ModelViewSet):

    queryset = Material.objects.select_related(
        "teaching_assignment",
        "teaching_assignment__teacher",
        "teaching_assignment__subject",
        "teaching_assignment__school_class",
    )

    serializer_class = MaterialSerializer

    permission_classes = [
        IsMaterialOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):

        teaching_assignment = (
            serializer.validated_data["teaching_assignment"]
        )

        if self.request.user.role == "teacher":

            if teaching_assignment.teacher.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied

                raise PermissionDenied(
                    "You can only create materials for your own teaching assignments."
                )

        serializer.save()

    def perform_update(self, serializer):

        teaching_assignment = (
            serializer.validated_data.get(
                "teaching_assignment",
                serializer.instance.teaching_assignment
            )
        )

        if self.request.user.role == "teacher":

            if teaching_assignment.teacher.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied

                raise PermissionDenied(
                    "You can only manage materials for your own teaching assignments."
                )

        serializer.save()


# ============================================================
# ASSIGNMENT
# ============================================================

class AssignmentViewSet(viewsets.ModelViewSet):

    queryset = Assignment.objects.select_related(
        "teaching_assignment",
        "teaching_assignment__teacher",
        "teaching_assignment__subject",
        "teaching_assignment__school_class",
    )

    serializer_class = AssignmentSerializer

    permission_classes = [
        IsAssignmentOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):

        teaching_assignment = (
            serializer.validated_data["teaching_assignment"]
        )

        if self.request.user.role == "teacher":

            if teaching_assignment.teacher.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied

                raise PermissionDenied(
                    "You can only create assignments for your own teaching assignments."
                )

        serializer.save()

    def perform_update(self, serializer):

        teaching_assignment = (
            serializer.validated_data.get(
                "teaching_assignment",
                serializer.instance.teaching_assignment
            )
        )

        if self.request.user.role == "teacher":

            if teaching_assignment.teacher.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied

                raise PermissionDenied(
                    "You can only manage assignments for your own teaching assignments."
                )

        serializer.save()


class AssignmentQuestionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentQuestion.objects.select_related(
        "assignment",
        "assignment__teaching_assignment",
        "assignment__teaching_assignment__teacher",
        "assignment__teaching_assignment__subject",
        "assignment__teaching_assignment__school_class",
    )
    serializer_class = AssignmentQuestionSerializer
    permission_classes = [IsAssignmentQuestionOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                assignment__teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        assignment = serializer.validated_data["assignment"]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only create questions for your own assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create an assignment question."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage questions for your own assignments."
                )

            new_assignment = serializer.validated_data.get(
                "assignment",
                instance.assignment
            )

            if (
                new_assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move questions to your own assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update an assignment question."
        )


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):

    queryset = AssignmentSubmission.objects.select_related(
        "assignment",
        "assignment__teaching_assignment",
        "assignment__teaching_assignment__teacher",
        "student",
    )

    serializer_class = AssignmentSubmissionSerializer

    permission_classes = [
        IsSubmissionOwnerOrTeacherOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                assignment__teaching_assignment__teacher__user=self.request.user
            )

        elif self.request.user.role == "student":
            queryset = queryset.filter(
                student__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):

        from rest_framework.exceptions import PermissionDenied

        assignment = serializer.validated_data["assignment"]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":
            raise PermissionDenied(
                "Teachers cannot create student submissions."
            )

        if self.request.user.role == "student":

            student = self.request.user.student_profile

            is_member = ClassMember.objects.filter(
                school_class=assignment.teaching_assignment.school_class,
                student=student,
                is_active=True,
            ).exists()

            if not is_member:
                raise PermissionDenied(
                    "You are not a member of the class for this assignment."
                )

            if not assignment.is_published:
                raise PermissionDenied(
                    "This assignment is not published."
                )

            serializer.save(
                student=student
            )

            return

        raise PermissionDenied(
            "You do not have permission to create a submission."
        )

    def perform_update(self, serializer):

        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage submissions for your own assignments."
                )

            serializer.save()
            return

        if self.request.user.role == "student":

            if instance.student.user != self.request.user:
                raise PermissionDenied(
                    "You can only manage your own submission."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update this submission."
        )


class SubmissionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SubmissionAnswer.objects.select_related(
        "submission",
        "submission__assignment",
        "submission__assignment__teaching_assignment",
        "submission__assignment__teaching_assignment__teacher",
        "submission__student",
        "question",
        "question__assignment",
    )
    serializer_class = SubmissionAnswerSerializer
    permission_classes = [IsSubmissionAnswerOwnerOrTeacherOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                submission__assignment__teaching_assignment__teacher__user=self.request.user
            )

        elif self.request.user.role == "student":
            queryset = queryset.filter(
                submission__student__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        submission = serializer.validated_data["submission"]
        question = serializer.validated_data["question"]

        # ====================================================
        # ADMIN
        # ====================================================

        if self.request.user.role == "admin":
            serializer.save()
            return

        # ====================================================
        # TEACHER
        # ====================================================

        if self.request.user.role == "teacher":

            if (
                submission.assignment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage answers for your own assignments."
                )

            serializer.save()
            return

        # ====================================================
        # STUDENT
        # ====================================================

        if self.request.user.role == "student":

            if submission.student.user != self.request.user:
                raise PermissionDenied(
                    "You can only answer your own submission."
                )

            if question.assignment_id != submission.assignment_id:
                raise PermissionDenied(
                    "This question does not belong to the submission assignment."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create an answer."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.submission.assignment
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage answers for your own assignments."
                )

            serializer.save()
            return

        if self.request.user.role == "student":

            if (
                instance.submission.student.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage your own answers."
                )

            new_submission = serializer.validated_data.get(
                "submission",
                instance.submission
            )

            new_question = serializer.validated_data.get(
                "question",
                instance.question
            )

            if new_submission.student.user != self.request.user:
                raise PermissionDenied(
                    "You can only manage your own answers."
                )

            if (
                new_question.assignment_id
                != new_submission.assignment_id
            ):
                raise PermissionDenied(
                    "The question must belong to the submission assignment."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update this answer."
        )


# ============================================================
# ASSESSMENT
# ============================================================

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.select_related(
        "teaching_assignment",
        "teaching_assignment__teacher",
        "teaching_assignment__subject",
        "teaching_assignment__school_class",
    )
    serializer_class = AssessmentSerializer
    permission_classes = [IsAssessmentOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        teaching_assignment = serializer.validated_data[
            "teaching_assignment"
        ]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only create assessments "
                    "for your own teaching assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create an assessment."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage your own assessments."
                )

            new_teaching_assignment = serializer.validated_data.get(
                "teaching_assignment",
                instance.teaching_assignment
            )

            if (
                new_teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move assessments "
                    "to your own teaching assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update this assessment."
        )


class AssessmentItemViewSet(viewsets.ModelViewSet):
    queryset = AssessmentItem.objects.select_related(
        "assessment",
        "assessment__teaching_assignment",
        "assessment__teaching_assignment__teacher",
        "assessment__teaching_assignment__subject",
        "assessment__teaching_assignment__school_class",
    )
    serializer_class = AssessmentItemSerializer
    permission_classes = [IsAssessmentItemOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                assessment__teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        assessment = serializer.validated_data["assessment"]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                assessment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only create assessment items "
                    "for your own assessments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create an assessment item."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.assessment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage items for your own assessments."
                )

            new_assessment = serializer.validated_data.get(
                "assessment",
                instance.assessment
            )

            if (
                new_assessment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move items to your own assessments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update this assessment item."
        )

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related(
        "assessment",
        "assessment__teaching_assignment",
        "assessment__teaching_assignment__teacher",
        "assessment__teaching_assignment__subject",
        "assessment__teaching_assignment__school_class",
        "student",
    )
    serializer_class = GradeSerializer
    permission_classes = [IsGradeOwnerOrTeacherOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                assessment__teaching_assignment__teacher__user=self.request.user
            )

        elif self.request.user.role == "student":
            queryset = queryset.filter(
                student__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        assessment = serializer.validated_data["assessment"]
        student = serializer.validated_data["student"]

        # ====================================================
        # ADMIN
        # ====================================================

        if self.request.user.role == "admin":
            serializer.save()
            return

        # ====================================================
        # TEACHER
        # ====================================================

        if self.request.user.role == "teacher":

            if (
                assessment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only create grades "
                    "for your own assessments."
                )

            is_member = ClassMember.objects.filter(
                school_class=(
                    assessment.teaching_assignment.school_class
                ),
                student=student,
                is_active=True,
            ).exists()

            if not is_member:
                raise PermissionDenied(
                    "You can only grade students "
                    "from the assessment class."
                )

            serializer.save()
            return

        # ====================================================
        # STUDENT
        # ====================================================

        if self.request.user.role == "student":
            raise PermissionDenied(
                "Students cannot create grades."
            )

        raise PermissionDenied(
            "You do not have permission to create a grade."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        # ====================================================
        # ADMIN
        # ====================================================

        if self.request.user.role == "admin":
            serializer.save()
            return

        # ====================================================
        # TEACHER
        # ====================================================

        if self.request.user.role == "teacher":

            if (
                instance.assessment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage grades "
                    "for your own assessments."
                )

            new_assessment = serializer.validated_data.get(
                "assessment",
                instance.assessment,
            )

            new_student = serializer.validated_data.get(
                "student",
                instance.student,
            )

            if (
                new_assessment.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move grades "
                    "to your own assessments."
                )

            is_member = ClassMember.objects.filter(
                school_class=(
                    new_assessment.teaching_assignment.school_class
                ),
                student=new_student,
                is_active=True,
            ).exists()

            if not is_member:
                raise PermissionDenied(
                    "The student must belong "
                    "to the assessment class."
                )

            serializer.save()
            return

        # ====================================================
        # STUDENT
        # ====================================================

        if self.request.user.role == "student":
            raise PermissionDenied(
                "Students cannot modify grades."
            )

        raise PermissionDenied(
            "You do not have permission to update this grade."
        )


class GradeComponentViewSet(viewsets.ModelViewSet):
    queryset = GradeComponent.objects.select_related(
        "teaching_assignment",
        "teaching_assignment__teacher",
        "teaching_assignment__subject",
        "teaching_assignment__school_class",
    )
    serializer_class = GradeComponentSerializer
    permission_classes = [IsGradeComponentOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        teaching_assignment = serializer.validated_data[
            "teaching_assignment"
        ]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only create grade components "
                    "for your own teaching assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create a grade component."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage your own grade components."
                )

            new_teaching_assignment = serializer.validated_data.get(
                "teaching_assignment",
                instance.teaching_assignment
            )

            if (
                new_teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move grade components "
                    "to your own teaching assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update this grade component."
        )


class ReportCardViewSet(viewsets.ModelViewSet):
    queryset = ReportCard.objects.select_related(
        "student",
        "student__user",
        "academic_year",
        "semester",
        "school_class",
    )
    serializer_class = ReportCardSerializer
    permission_classes = [IsReportCardOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "student":
            queryset = queryset.filter(
                student__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can create report cards."
            )

        serializer.save()

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can update report cards."
            )

        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can delete report cards."
            )

        instance.delete()


# ============================================================
# SCHEDULE
# ============================================================

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related(
        "teaching_assignment",
        "teaching_assignment__teacher",
        "teaching_assignment__subject",
        "teaching_assignment__school_class",
    )
    serializer_class = ScheduleSerializer
    permission_classes = [IsScheduleOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        teaching_assignment = serializer.validated_data[
            "teaching_assignment"
        ]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only create schedules "
                    "for your own teaching assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create a schedule."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage your own schedules."
                )

            new_teaching_assignment = serializer.validated_data.get(
                "teaching_assignment",
                instance.teaching_assignment
            )

            if (
                new_teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move schedules "
                    "to your own teaching assignments."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update this schedule."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if self.request.user.role == "teacher":

            if (
                instance.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only delete your own schedules."
                )

            instance.delete()
            return

        raise PermissionDenied(
            "You do not have permission to delete this schedule."
        )


# ============================================================
# SCHOOL ATTENDANCE
# ============================================================

class SchoolAttendanceSessionViewSet(
    viewsets.ModelViewSet
):

    queryset = SchoolAttendanceSession.objects.select_related(
        "school",
    )

    serializer_class = SchoolAttendanceSessionSerializer

    permission_classes = [
        IsSchoolAttendanceSessionOwnerOrAdmin
    ]

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role in {"admin", "teacher"}:
            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create "
            "a school attendance session."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role in {"admin", "teacher"}:
            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update "
            "a school attendance session."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role in {"admin", "teacher"}:
            instance.delete()
            return

        raise PermissionDenied(
            "You do not have permission to delete "
            "a school attendance session."
        )


class SchoolAttendanceRecordViewSet(
    viewsets.ModelViewSet
):

    queryset = SchoolAttendanceRecord.objects.select_related(
        "session",
        "session__school",
        "student",
        "student__user",
    )

    serializer_class = SchoolAttendanceRecordSerializer

    permission_classes = [
        IsSchoolAttendanceRecordOwnerOrTeacherOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "student":
            queryset = queryset.filter(
                student__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        session = serializer.validated_data["session"]
        student = serializer.validated_data["student"]

        # ADMIN
        if self.request.user.role == "admin":
            serializer.save()
            return

        # TEACHER
        if self.request.user.role == "teacher":

            teacher_profile = getattr(
                self.request.user,
                "teacher_profile",
                None,
            )

            if teacher_profile is None:
                raise PermissionDenied(
                    "Teacher profile not found."
                )

            if student.school_id != session.school_id:
                raise PermissionDenied(
                    "Student does not belong to "
                    "the attendance school."
                )

            serializer.save()
            return

        # STUDENT
        if self.request.user.role == "student":
            raise PermissionDenied(
                "Students cannot create school attendance records."
            )

        raise PermissionDenied(
            "You do not have permission to create "
            "a school attendance record."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        # ADMIN
        if self.request.user.role == "admin":
            serializer.save()
            return

        # TEACHER
        if self.request.user.role == "teacher":

            session = serializer.validated_data.get(
                "session",
                instance.session,
            )

            student = serializer.validated_data.get(
                "student",
                instance.student,
            )

            if student.school_id != session.school_id:
                raise PermissionDenied(
                    "Student does not belong to "
                    "the attendance school."
                )

            serializer.save()
            return

        # STUDENT
        if self.request.user.role == "student":
            raise PermissionDenied(
                "Students cannot modify "
                "school attendance records."
            )

        raise PermissionDenied(
            "You do not have permission to update "
            "this attendance record."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role in {
            "admin",
            "teacher",
        }:
            instance.delete()
            return

        raise PermissionDenied(
            "You do not have permission to delete "
            "this attendance record."
        )


# ============================================================
# CLASS ATTENDANCE
# ============================================================

class ClassAttendanceSessionViewSet(viewsets.ModelViewSet):
    queryset = ClassAttendanceSession.objects.select_related(
        "schedule",
        "schedule__teaching_assignment",
        "schedule__teaching_assignment__teacher",
        "schedule__teaching_assignment__subject",
        "schedule__teaching_assignment__school_class",
    )
    serializer_class = ClassAttendanceSessionSerializer
    permission_classes = [IsClassAttendanceSessionOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                schedule__teaching_assignment__teacher__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        schedule = serializer.validated_data["schedule"]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                schedule.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only create attendance sessions "
                    "for your own schedules."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to create "
            "a class attendance session."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":

            if (
                instance.schedule.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage your own attendance sessions."
                )

            new_schedule = serializer.validated_data.get(
                "schedule",
                instance.schedule
            )

            if (
                new_schedule.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move attendance sessions "
                    "to your own schedules."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update "
            "this attendance session."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if self.request.user.role == "teacher":

            if (
                instance.schedule.teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only delete your own attendance sessions."
                )

            instance.delete()
            return

        raise PermissionDenied(
            "You do not have permission to delete "
            "this attendance session."
        )


class ClassAttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = ClassAttendanceRecord.objects.select_related(
        "session",
        "session__schedule",
        "session__schedule__teaching_assignment",
        "session__schedule__teaching_assignment__teacher",
        "session__schedule__teaching_assignment__subject",
        "session__schedule__teaching_assignment__school_class",
        "student",
    )
    serializer_class = ClassAttendanceRecordSerializer
    permission_classes = [
        IsClassAttendanceRecordOwnerOrTeacherOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                session__schedule__teaching_assignment__teacher__user=
                self.request.user
            )

        elif self.request.user.role == "student":
            queryset = queryset.filter(
                student__user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        session = serializer.validated_data["session"]
        student = serializer.validated_data["student"]

        # ====================================================
        # ADMIN
        # ====================================================

        if self.request.user.role == "admin":
            serializer.save()
            return

        # ====================================================
        # TEACHER
        # ====================================================

        if self.request.user.role == "teacher":

            if (
                session.schedule
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage attendance "
                    "for your own schedules."
                )

            is_member = ClassMember.objects.filter(
                school_class=(
                    session.schedule
                    .teaching_assignment
                    .school_class
                ),
                student=student,
                is_active=True,
            ).exists()

            if not is_member:
                raise PermissionDenied(
                    "You can only record attendance "
                    "for students in the scheduled class."
                )

            serializer.save()
            return

        # ====================================================
        # STUDENT
        # ====================================================

        if self.request.user.role == "student":
            raise PermissionDenied(
                "Students cannot create attendance records."
            )

        raise PermissionDenied(
            "You do not have permission to create "
            "an attendance record."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        # ====================================================
        # ADMIN
        # ====================================================

        if self.request.user.role == "admin":
            serializer.save()
            return

        # ====================================================
        # TEACHER
        # ====================================================

        if self.request.user.role == "teacher":

            if (
                instance.session.schedule
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only manage attendance "
                    "for your own schedules."
                )

            new_session = serializer.validated_data.get(
                "session",
                instance.session
            )

            new_student = serializer.validated_data.get(
                "student",
                instance.student
            )

            if (
                new_session.schedule
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only move attendance "
                    "to your own schedules."
                )

            is_member = ClassMember.objects.filter(
                school_class=(
                    new_session.schedule
                    .teaching_assignment
                    .school_class
                ),
                student=new_student,
                is_active=True,
            ).exists()

            if not is_member:
                raise PermissionDenied(
                    "The student must belong "
                    "to the scheduled class."
                )

            serializer.save()
            return

        # ====================================================
        # STUDENT
        # ====================================================

        if self.request.user.role == "student":
            raise PermissionDenied(
                "Students cannot modify attendance records."
            )

        raise PermissionDenied(
            "You do not have permission to update "
            "this attendance record."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if self.request.user.role == "teacher":

            if (
                instance.session.schedule
                .teaching_assignment.teacher.user
                != self.request.user
            ):
                raise PermissionDenied(
                    "You can only delete attendance "
                    "records for your own schedules."
                )

            instance.delete()
            return

        raise PermissionDenied(
            "You do not have permission to delete "
            "this attendance record."
        )


# ============================================================
# ANNOUNCEMENT
# ============================================================

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related(
        "created_by",
    )
    serializer_class = AnnouncementSerializer
    permission_classes = [
        IsAnnouncementOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "teacher":
            queryset = queryset.filter(
                created_by=self.request.user
            )

        elif self.request.user.role == "student":
            queryset = queryset.filter(
                target__in=[
                    "public",
                    "student",
                    "all",
                ],
                is_published=True,
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            serializer.save(
                created_by=self.request.user
            )
            return

        if self.request.user.role == "teacher":
            serializer.save(
                created_by=self.request.user
            )
            return

        raise PermissionDenied(
            "You do not have permission to create "
            "an announcement."
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if self.request.user.role == "teacher":
            if instance.created_by != self.request.user:
                raise PermissionDenied(
                    "You can only manage your own announcements."
                )

            serializer.save()
            return

        raise PermissionDenied(
            "You do not have permission to update "
            "this announcement."
        )

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if self.request.user.role == "teacher":
            if instance.created_by != self.request.user:
                raise PermissionDenied(
                    "You can only delete your own announcements."
                )

            instance.delete()
            return

        raise PermissionDenied(
            "You do not have permission to delete "
            "this announcement."
        )


# ============================================================
# NOTIFICATION
# ============================================================

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related(
        "user",
    )
    serializer_class = NotificationSerializer
    permission_classes = [
        IsNotificationOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role in {
            "teacher",
            "student",
        }:
            queryset = queryset.filter(
                user=self.request.user
            )

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can create notifications."
            )

        serializer.save()

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Users cannot directly update notifications."
            )

        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Users cannot delete notifications."
            )

        instance.delete()

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-read",
    )
    def mark_read(self, request, pk=None):
        notification = self.get_object()

        if request.user.role != "admin":
            if notification.user != request.user:
                raise PermissionDenied(
                    "You can only mark your own notifications as read."
                )

        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save(
                update_fields=[
                    "is_read",
                    "read_at",
                ]
            )

        return Response(
            {
                "detail": "Notification marked as read."
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# COMMUNICATION
# ============================================================

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.select_related(
        "created_by",
    ).prefetch_related(
        "members__user",
    )
    serializer_class = ConversationSerializer
    permission_classes = [
        IsConversationMemberOrOwnerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role != "admin":
            queryset = queryset.filter(
                Q(created_by=self.request.user)
                | Q(members__user=self.request.user)
            ).distinct()

        return queryset

    def perform_create(self, serializer):
        conversation = serializer.save(
            created_by=self.request.user
        )

        ConversationMember.objects.get_or_create(
            conversation=conversation,
            user=self.request.user,
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if instance.created_by != self.request.user:
            raise PermissionDenied(
                "Only the conversation creator can update "
                "this conversation."
            )

        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if instance.created_by != self.request.user:
            raise PermissionDenied(
                "Only the conversation creator can delete "
                "this conversation."
            )

        instance.delete()


class ConversationMemberViewSet(viewsets.ModelViewSet):
    queryset = ConversationMember.objects.select_related(
        "conversation",
        "conversation__created_by",
        "user",
    )
    serializer_class = ConversationMemberSerializer
    permission_classes = [
        IsConversationMemberManagerOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role != "admin":
            queryset = queryset.filter(
                Q(conversation__created_by=self.request.user)
                | Q(user=self.request.user)
            ).distinct()

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        conversation = serializer.validated_data["conversation"]

        if self.request.user.role == "admin":
            serializer.save()
            return

        if conversation.created_by != self.request.user:
            raise PermissionDenied(
                "Only the conversation creator can add members."
            )

        serializer.save()

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        instance = serializer.instance

        if self.request.user.role == "admin":
            serializer.save()
            return

        if instance.conversation.created_by != self.request.user:
            raise PermissionDenied(
                "Only the conversation creator can update members."
            )

        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role == "admin":
            instance.delete()
            return

        if instance.conversation.created_by != self.request.user:
            raise PermissionDenied(
                "Only the conversation creator can remove members."
            )

        instance.delete()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related(
        "conversation",
        "sender",
    )
    serializer_class = MessageSerializer
    permission_classes = [
        IsMessageMemberOrAdmin
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role != "admin":
            queryset = queryset.filter(
                conversation__members__user=self.request.user
            ).distinct()

        return queryset

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        conversation = serializer.validated_data["conversation"]

        if self.request.user.role == "admin":
            serializer.save(
                sender=self.request.user
            )
            return

        is_member = conversation.members.filter(
            user=self.request.user
        ).exists()

        if not is_member:
            raise PermissionDenied(
                "You must be a member of the conversation "
                "to send a message."
            )

        serializer.save(
            sender=self.request.user
        )

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Messages cannot be modified."
            )

        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Messages cannot be deleted."
            )

        instance.delete()


# ============================================================
# SYSTEM
# ============================================================

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = [
        IsSettingAdminOrReadOnly
    ]

    def perform_create(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can create settings."
            )

        serializer.save()

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can update settings."
            )

        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied

        if self.request.user.role != "admin":
            raise PermissionDenied(
                "Only administrators can delete settings."
            )

        instance.delete()


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related(
        "user",
    )
    serializer_class = ActivityLogSerializer
    permission_classes = [
        IsAdminActivityLog
    ]


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related(
        "user",
    )
    serializer_class = AuditLogSerializer
    permission_classes = [
        IsAdminAuditLog
    ]


# ============================================================
# AUTHENTICATION
# ============================================================

class CustomAuthToken(ObtainAuthToken):

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={
                "request": request
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "token": token.key,
                "role": user.role,
                "user_id": user.pk,
                "full_name": user.full_name,
            }
        )

