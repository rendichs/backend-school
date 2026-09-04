from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

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


# ============================================================
# USER
# ============================================================

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "role",
            "full_name",
            "is_active",
        ]

        read_only_fields = [
            "id",
        ]


# ============================================================
# SCHOOL
# ============================================================

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# TEACHER
# ============================================================

class TeacherSerializer(serializers.ModelSerializer):

    employee_number = serializers.CharField(
        source="teacher_profile.employee_number"
    )

    gender = serializers.CharField(
        source="teacher_profile.gender"
    )

    phone = serializers.CharField(
        source="teacher_profile.phone",
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    address = serializers.CharField(
        source="teacher_profile.address",
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    school = serializers.PrimaryKeyRelatedField(
        source="teacher_profile.school",
        queryset=School.objects.all(),
    )

    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
    )

    class Meta:
        model = CustomUser

        fields = [
            "id",
            "username",
            "email",
            "password",
            "full_name",
            "role",
            "employee_number",
            "gender",
            "phone",
            "address",
            "school",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "role",
        ]

    def create(self, validated_data):

        profile_data = validated_data.pop(
            "teacher_profile"
        )

        password = validated_data.pop(
            "password",
            None
        )

        if not password:
            raise serializers.ValidationError({
                "password": "Password is required."
            })

        user = CustomUser(
            **validated_data,
            role="teacher",
        )

        user.set_password(password)
        user.save()

        TeacherProfile.objects.create(
            user=user,
            **profile_data,
        )

        return user

    def update(self, instance, validated_data):

        profile_data = validated_data.pop(
            "teacher_profile",
            {}
        )

        password = validated_data.pop(
            "password",
            None
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        profile = instance.teacher_profile

        for attr, value in profile_data.items():
            setattr(profile, attr, value)

        profile.save()

        return instance


# ============================================================
# STUDENT
# ============================================================

class StudentSerializer(serializers.ModelSerializer):

    student_number = serializers.CharField(
        source="student_profile.student_number"
    )

    gender = serializers.CharField(
        source="student_profile.gender"
    )

    date_of_birth = serializers.DateField(
        source="student_profile.date_of_birth",
        required=False,
        allow_null=True,
    )

    address = serializers.CharField(
        source="student_profile.address",
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    school = serializers.PrimaryKeyRelatedField(
        source="student_profile.school",
        queryset=School.objects.all(),
    )

    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
    )

    class Meta:
        model = CustomUser

        fields = [
            "id",
            "username",
            "email",
            "password",
            "full_name",
            "role",
            "student_number",
            "gender",
            "date_of_birth",
            "address",
            "school",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "role",
        ]

    def create(self, validated_data):

        profile_data = validated_data.pop(
            "student_profile"
        )

        password = validated_data.pop(
            "password",
            None
        )

        if not password:
            raise serializers.ValidationError({
                "password": "Password is required."
            })

        user = CustomUser(
            **validated_data,
            role="student",
        )

        user.set_password(password)
        user.save()

        StudentProfile.objects.create(
            user=user,
            **profile_data,
        )

        return user

    def update(self, instance, validated_data):

        profile_data = validated_data.pop(
            "student_profile",
            {}
        )

        password = validated_data.pop(
            "password",
            None
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        profile = instance.student_profile

        for attr, value in profile_data.items():
            setattr(profile, attr, value)

        profile.save()

        return instance


# ============================================================
# ACADEMIC
# ============================================================

class AcademicYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcademicYear
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class InterestClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterestClass
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SchoolClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolClass
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        grade_level = attrs.get(
            "grade_level",
            getattr(
                self.instance,
                "grade_level",
                None
            )
        )

        interest_class = attrs.get(
            "interest_class",
            getattr(
                self.instance,
                "interest_class",
                None
            )
        )

        # Grade 11 dan 12 wajib memiliki interest class
        if grade_level in [11, 12] and not interest_class:
            raise serializers.ValidationError({
                "interest_class": (
                    "Interest class is required for Grade 11 and Grade 12."
                )
            })

        # Grade 10 belum memiliki interest class
        if grade_level == 10 and interest_class:
            raise serializers.ValidationError({
                "interest_class": (
                    "Grade 10 cannot have an interest class."
                )
            })

        return attrs


class ClassMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassMember
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "joined_at",
        ]


# ============================================================
# SUBJECT
# ============================================================

class SubjectGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectGroup
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# TEACHING ASSIGNMENT
# ============================================================

class TeachingAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeachingAssignment

        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        teacher = attrs.get(
            "teacher",
            getattr(
                self.instance,
                "teacher",
                None
            )
        )

        subject = attrs.get(
            "subject",
            getattr(
                self.instance,
                "subject",
                None
            )
        )

        school_class = attrs.get(
            "school_class",
            getattr(
                self.instance,
                "school_class",
                None
            )
        )

        academic_year = attrs.get(
            "academic_year",
            getattr(
                self.instance,
                "academic_year",
                None
            )
        )

        semester = attrs.get(
            "semester",
            getattr(
                self.instance,
                "semester",
                None
            )
        )

        errors = {}

        # ====================================================
        # 1. TEACHER ↔ SCHOOL CLASS
        # ====================================================

        if teacher and school_class:

            teacher_school_id = teacher.school_id

            class_school_id = (
                school_class.program.school_id
            )

            if teacher_school_id != class_school_id:
                errors["teacher"] = (
                    "Teacher and class must belong "
                    "to the same school."
                )

        # ====================================================
        # 2. SUBJECT ↔ SCHOOL CLASS
        # ====================================================

        if subject and school_class:

            subject_school_id = subject.school_id

            class_school_id = (
                school_class.program.school_id
            )

            if subject_school_id != class_school_id:
                errors["subject"] = (
                    "Subject and class must belong "
                    "to the same school."
                )

        # ====================================================
        # 3. CLASS ↔ ACADEMIC YEAR
        # ====================================================

        if school_class and academic_year:

            if school_class.academic_year_id != academic_year.id:
                errors["academic_year"] = (
                    "Academic year must match "
                    "the class academic year."
                )

        # ====================================================
        # 4. SEMESTER ↔ ACADEMIC YEAR
        # ====================================================

        if semester and academic_year:

            if semester.academic_year_id != academic_year.id:
                errors["semester"] = (
                    "Semester must belong "
                    "to the selected academic year."
                )

        # ====================================================
        # RETURN VALIDATION ERRORS
        # ====================================================

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

# ============================================================
# FILE
# ============================================================

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"

        read_only_fields = [
            "id",
            "uploaded_by",
            "uploaded_at",
        ]


class MaterialFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialFile
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return attrs

        if request.user.role == "admin":
            return attrs

        material = attrs.get(
            "material",
            getattr(self.instance, "material", None),
        )

        file_obj = attrs.get(
            "file",
            getattr(self.instance, "file", None),
        )

        if request.user.role == "teacher":
            if (
                material.teaching_assignment.teacher.user
                != request.user
            ):
                raise serializers.ValidationError({
                    "material": (
                        "You can only manage files "
                        "of your own materials."
                    )
                })

            if file_obj.uploaded_by != request.user:
                raise serializers.ValidationError({
                    "file": (
                        "You can only attach files "
                        "uploaded by yourself."
                    )
                })

        return attrs


class AssignmentFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentFile
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return attrs

        if request.user.role == "admin":
            return attrs

        assignment = attrs.get(
            "assignment",
            getattr(self.instance, "assignment", None),
        )

        file_obj = attrs.get(
            "file",
            getattr(self.instance, "file", None),
        )

        if request.user.role == "teacher":
            if (
                assignment.teaching_assignment.teacher.user
                != request.user
            ):
                raise serializers.ValidationError({
                    "assignment": (
                        "You can only manage files "
                        "of your own assignments."
                    )
                })

            if file_obj.uploaded_by != request.user:
                raise serializers.ValidationError({
                    "file": (
                        "You can only attach files "
                        "uploaded by yourself."
                    )
                })

        return attrs


class SubmissionFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubmissionFile
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return attrs

        if request.user.role == "admin":
            return attrs

        submission = attrs.get(
            "submission",
            getattr(self.instance, "submission", None),
        )

        file_obj = attrs.get(
            "file",
            getattr(self.instance, "file", None),
        )

        if request.user.role == "teacher":
            if (
                submission.assignment
                .teaching_assignment.teacher.user
                != request.user
            ):
                raise serializers.ValidationError({
                    "submission": (
                        "You can only manage files "
                        "of your own assignments."
                    )
                })

            if file_obj.uploaded_by != request.user:
                raise serializers.ValidationError({
                    "file": (
                        "You can only attach files "
                        "uploaded by yourself."
                    )
                })

        elif request.user.role == "student":
            if (
                submission.student.user
                != request.user
            ):
                raise serializers.ValidationError({
                    "submission": (
                        "You can only manage files "
                        "of your own submission."
                    )
                })

            if file_obj.uploaded_by != request.user:
                raise serializers.ValidationError({
                    "file": (
                        "You can only attach files "
                        "uploaded by yourself."
                    )
                })

        return attrs


# ============================================================
# MATERIAL
# ============================================================

class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# ASSIGNMENT
# ============================================================

class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class AssignmentQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentQuestion
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


class AssignmentSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignmentSubmission
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "graded_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return attrs

        role = request.user.role

        # ====================================================
        # STUDENT
        # ====================================================

        if role == "student":

            forbidden_fields = {
                "student",
                "status",
                "score",
                "feedback",
                "graded_at",
            }

            submitted_fields = (
                forbidden_fields
                & set(attrs.keys())
            )

            if submitted_fields:

                field = sorted(submitted_fields)[0]

                raise serializers.ValidationError({
                    field: (
                        f"Students cannot set '{field}'."
                    )
                })

        # ====================================================
        # TEACHER
        # ====================================================

        elif role == "teacher":

            if "student" in attrs:

                raise serializers.ValidationError({
                    "student": (
                        "Teachers cannot change the submission student."
                    )
                })

        return attrs


class SubmissionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubmissionAnswer
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# ASSESSMENT
# ============================================================

class AssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class AssessmentItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentItem
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return attrs

        role = request.user.role

        # ====================================================
        # STUDENT
        # ====================================================

        if role == "student":
            raise serializers.ValidationError(
                "Students cannot create or modify grades."
            )

        # ====================================================
        # TEACHER
        # ====================================================

        if role == "teacher":

            if "student" in attrs:
                student = attrs["student"]

                assessment = attrs.get(
                    "assessment",
                    getattr(
                        self.instance,
                        "assessment",
                        None,
                    ),
                )

                if assessment:
                    is_member = ClassMember.objects.filter(
                        school_class=(
                            assessment
                            .teaching_assignment
                            .school_class
                        ),
                        student=student,
                        is_active=True,
                    ).exists()

                    if not is_member:
                        raise serializers.ValidationError({
                            "student": (
                                "The student must belong "
                                "to the assessment class."
                            )
                        })

        return attrs


class GradeComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeComponent
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ReportCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportCard
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# SCHEDULE
# ============================================================

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# SCHOOL ATTENDANCE
# ============================================================

class SchoolAttendanceSessionSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = SchoolAttendanceSession
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SchoolAttendanceRecordSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = SchoolAttendanceRecord
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# CLASS ATTENDANCE
# ============================================================

class ClassAttendanceSessionSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ClassAttendanceSession
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ClassAttendanceRecordSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ClassAttendanceRecord
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# ANNOUNCEMENT
# ============================================================

class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# NOTIFICATION
# ============================================================

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


# ============================================================
# COMMUNICATION
# ============================================================

class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ConversationMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConversationMember
        fields = "__all__"

        read_only_fields = [
            "id",
            "joined_at",
        ]


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"

        read_only_fields = [
            "id",
            "sent_at",
        ]


# ============================================================
# SYSTEM
# ============================================================

class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setting
        fields = "__all__"

        read_only_fields = [
            "id",
            "updated_at",
        ]


class ActivityLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityLog
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


class AuditLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuditLog
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


# ============================================================
# AUTHENTICATION
# ============================================================

class CustomAuthTokenSerializer(AuthTokenSerializer):

    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if user:
            attrs["user"] = user
            return attrs

        inactive_user = CustomUser.objects.filter(
            username=username
        ).first()

        if inactive_user and not inactive_user.is_active:
            raise serializers.ValidationError({
                "detail": (
                    "Your account is currently disabled. "
                    "Please contact the administrator."
                )
            })

        raise serializers.ValidationError({
            "detail": "Invalid username or password."
        })