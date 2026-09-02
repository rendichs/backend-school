from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    TeacherViewSet,
    StudentViewSet,
    SchoolViewSet,
    AcademicYearViewSet,
    SemesterViewSet,
    ProgramViewSet,
    InterestClassViewSet,
    SchoolClassViewSet,
    SubjectViewSet,
    TeachingAssignmentViewSet,
    MaterialViewSet,
    AssignmentViewSet,
    AssessmentViewSet,
    GradeViewSet,
    ScheduleViewSet,
    SchoolAttendanceSessionViewSet,
    ClassAttendanceSessionViewSet,
    AnnouncementViewSet,
)

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user")

router.register(
    r"teachers",
    TeacherViewSet,
    basename="teacher",
)

router.register(
    r"students",
    StudentViewSet,
    basename="student",
)

router.register(
    r"schools",
    SchoolViewSet,
    basename="school",
)

router.register(
    r"academic-years",
    AcademicYearViewSet,
    basename="academic-year",
)

router.register(
    r"semesters",
    SemesterViewSet,
    basename="semester",
)

router.register(
    r"programs",
    ProgramViewSet,
    basename="program",
)

router.register(
    r"interest-classes",
    InterestClassViewSet,
    basename="interest-class",
)

router.register(
    r"classes",
    SchoolClassViewSet,
    basename="school-class",
)

router.register(
    r"subjects",
    SubjectViewSet,
    basename="subject",
)

router.register(
    r"teaching-assignments",
    TeachingAssignmentViewSet,
    basename="teaching-assignment",
)

router.register(
    r"materials",
    MaterialViewSet,
    basename="material",
)

router.register(
    r"assignments",
    AssignmentViewSet,
    basename="assignment",
)

router.register(
    r"assessments",
    AssessmentViewSet,
    basename="assessment",
)

router.register(
    r"grades",
    GradeViewSet,
    basename="grade",
)

router.register(
    r"schedules",
    ScheduleViewSet,
    basename="schedule",
)

router.register(
    r"school-attendance-sessions",
    SchoolAttendanceSessionViewSet,
    basename="school-attendance-session",
)

router.register(
    r"class-attendance-sessions",
    ClassAttendanceSessionViewSet,
    basename="class-attendance-session",
)

router.register(
    r"announcements",
    AnnouncementViewSet,
    basename="announcement",
)


urlpatterns = [
    path("", include(router.urls)),
]