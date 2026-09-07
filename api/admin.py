from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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

admin.site.register(CustomUser, UserAdmin)

admin.site.register(School)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)

admin.site.register(AcademicYear)
admin.site.register(Semester)

admin.site.register(Program)
admin.site.register(InterestClass)
admin.site.register(SchoolClass)
admin.site.register(ClassMember)

admin.site.register(SubjectGroup)
admin.site.register(Subject)
admin.site.register(TeachingAssignment)

admin.site.register(File)

admin.site.register(Material)
admin.site.register(MaterialFile)

admin.site.register(Assignment)
admin.site.register(AssignmentFile)
admin.site.register(AssignmentQuestion)
admin.site.register(AssignmentSubmission)
admin.site.register(SubmissionAnswer)
admin.site.register(SubmissionFile)

admin.site.register(Assessment)
admin.site.register(AssessmentItem)
admin.site.register(Grade)
admin.site.register(GradeComponent)
admin.site.register(ReportCard)

admin.site.register(Schedule)

admin.site.register(SchoolAttendanceSession)
admin.site.register(SchoolAttendanceRecord)

admin.site.register(ClassAttendanceSession)
admin.site.register(ClassAttendanceRecord)

admin.site.register(Announcement)
admin.site.register(Notification)

admin.site.register(Conversation)
admin.site.register(ConversationMember)
admin.site.register(Message)

admin.site.register(Setting)

admin.site.register(ActivityLog)
admin.site.register(AuditLog)