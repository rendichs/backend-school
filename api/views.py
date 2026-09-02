from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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

    queryset = File.objects.all()

    serializer_class = FileSerializer

    permission_classes = [
        IsAdminOrTeacherRole
    ]


class MaterialFileViewSet(viewsets.ModelViewSet):

    queryset = MaterialFile.objects.all()

    serializer_class = MaterialFileSerializer

    permission_classes = [
        IsAdminOrTeacherWriteReadOnly
    ]


class AssignmentFileViewSet(viewsets.ModelViewSet):

    queryset = AssignmentFile.objects.all()

    serializer_class = AssignmentFileSerializer

    permission_classes = [
        IsAuthenticated
    ]


class SubmissionFileViewSet(viewsets.ModelViewSet):

    queryset = SubmissionFile.objects.all()

    serializer_class = SubmissionFileSerializer

    permission_classes = [
        IsAuthenticated
    ]


# ============================================================
# MATERIAL
# ============================================================

class MaterialViewSet(viewsets.ModelViewSet):

    queryset = Material.objects.select_related(
        "teaching_assignment"
    )

    serializer_class = MaterialSerializer

    permission_classes = [
        IsAuthenticated
    ]


# ============================================================
# ASSIGNMENT
# ============================================================

class AssignmentViewSet(viewsets.ModelViewSet):

    queryset = Assignment.objects.select_related(
        "teaching_assignment"
    )

    serializer_class = AssignmentSerializer

    permission_classes = [
        IsAdminOrTeacherWriteReadOnly
    ]


class AssignmentQuestionViewSet(viewsets.ModelViewSet):

    queryset = AssignmentQuestion.objects.all()

    serializer_class = AssignmentQuestionSerializer

    permission_classes = [
        IsAuthenticated
    ]


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):

    queryset = AssignmentSubmission.objects.select_related(
        "assignment",
        "student",
    )

    serializer_class = AssignmentSubmissionSerializer

    permission_classes = [
        IsAuthenticatedApplicationUser
    ]


class SubmissionAnswerViewSet(viewsets.ModelViewSet):

    queryset = SubmissionAnswer.objects.all()

    serializer_class = SubmissionAnswerSerializer

    permission_classes = [
        IsAuthenticated
    ]


# ============================================================
# ASSESSMENT
# ============================================================

class AssessmentViewSet(viewsets.ModelViewSet):

    queryset = Assessment.objects.select_related(
        "teaching_assignment"
    )

    serializer_class = AssessmentSerializer

    permission_classes = [
        IsAuthenticated
    ]


class AssessmentItemViewSet(viewsets.ModelViewSet):

    queryset = AssessmentItem.objects.all()

    serializer_class = AssessmentItemSerializer

    permission_classes = [
        IsAuthenticated
    ]


class GradeViewSet(viewsets.ModelViewSet):

    queryset = Grade.objects.select_related(
        "assessment",
        "student",
    )

    serializer_class = GradeSerializer

    permission_classes = [
        IsAuthenticatedApplicationUser
    ]


class GradeComponentViewSet(viewsets.ModelViewSet):

    queryset = GradeComponent.objects.all()

    serializer_class = GradeComponentSerializer

    permission_classes = [
        IsAuthenticated
    ]


class ReportCardViewSet(viewsets.ModelViewSet):

    queryset = ReportCard.objects.select_related(
        "student",
        "school_class",
        "academic_year",
        "semester",
    )

    serializer_class = ReportCardSerializer

    permission_classes = [
        IsAuthenticated
    ]


# ============================================================
# SCHEDULE
# ============================================================

class ScheduleViewSet(viewsets.ModelViewSet):

    queryset = Schedule.objects.select_related(
        "teaching_assignment"
    )

    serializer_class = ScheduleSerializer

    permission_classes = [
        IsAdminUserRole
    ]


# ============================================================
# SCHOOL ATTENDANCE
# ============================================================

class SchoolAttendanceSessionViewSet(
    viewsets.ModelViewSet
):

    queryset = SchoolAttendanceSession.objects.all()

    serializer_class = SchoolAttendanceSessionSerializer

    permission_classes = [
        IsAdminOrTeacherRole
    ]


class SchoolAttendanceRecordViewSet(
    viewsets.ModelViewSet
):

    queryset = SchoolAttendanceRecord.objects.select_related(
        "session",
        "student",
    )

    serializer_class = SchoolAttendanceRecordSerializer

    permission_classes = [
        IsAdminOrTeacherRole
    ]


# ============================================================
# CLASS ATTENDANCE
# ============================================================

class ClassAttendanceSessionViewSet(
    viewsets.ModelViewSet
):

    queryset = ClassAttendanceSession.objects.select_related(
        "schedule"
    )

    serializer_class = ClassAttendanceSessionSerializer

    permission_classes = [
        IsAdminOrTeacherRole
    ]


class ClassAttendanceRecordViewSet(
    viewsets.ModelViewSet
):

    queryset = ClassAttendanceRecord.objects.select_related(
        "session",
        "student",
    )

    serializer_class = ClassAttendanceRecordSerializer

    permission_classes = [
        IsAdminOrTeacherRole
    ]


# ============================================================
# ANNOUNCEMENT
# ============================================================

class AnnouncementViewSet(viewsets.ModelViewSet):

    queryset = Announcement.objects.select_related(
        "created_by"
    )

    serializer_class = AnnouncementSerializer

    permission_classes = [
        IsAdminOrTeacherRole
    ]


# ============================================================
# NOTIFICATION
# ============================================================

class NotificationViewSet(viewsets.ModelViewSet):

    queryset = Notification.objects.select_related(
        "user"
    )

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated
    ]


# ============================================================
# COMMUNICATION
# ============================================================

class ConversationViewSet(viewsets.ModelViewSet):

    queryset = Conversation.objects.all()

    serializer_class = ConversationSerializer

    permission_classes = [
        IsAuthenticated
    ]


class ConversationMemberViewSet(
    viewsets.ModelViewSet
):

    queryset = ConversationMember.objects.select_related(
        "conversation",
        "user",
    )

    serializer_class = ConversationMemberSerializer

    permission_classes = [
        IsAuthenticated
    ]


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.select_related(
        "conversation",
        "sender",
    )

    serializer_class = MessageSerializer

    permission_classes = [
        IsAuthenticated
    ]


# ============================================================
# SYSTEM
# ============================================================

class SettingViewSet(viewsets.ModelViewSet):

    queryset = Setting.objects.all()

    serializer_class = SettingSerializer

    permission_classes = [
        IsAuthenticated
    ]


class ActivityLogViewSet(viewsets.ModelViewSet):

    queryset = ActivityLog.objects.all()

    serializer_class = ActivityLogSerializer

    permission_classes = [
        IsAuthenticated
    ]


class AuditLogViewSet(viewsets.ModelViewSet):

    queryset = AuditLog.objects.all()

    serializer_class = AuditLogSerializer

    permission_classes = [
        IsAuthenticated
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