from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


# ============================================================
# USER & AUTHENTICATION
# ============================================================

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        return self.create_user(
            username,
            email,
            password,
            **extra_fields
        )


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
    )

    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.full_name or self.username


# ============================================================
# SCHOOL MASTER
# ============================================================

class School(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=50,
        unique=True,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "schools"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# USER PROFILES
# ============================================================

class TeacherProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        limit_choices_to={"role": "teacher"},
    )

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="teachers",
    )

    employee_number = models.CharField(
        max_length=50,
        unique=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "teacher_profiles"
        ordering = ["employee_number"]

    def __str__(self):
        return self.employee_number


class StudentProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile",
        limit_choices_to={"role": "student"},
    )

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="students",
    )

    student_number = models.CharField(
        max_length=50,
        unique=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_profiles"
        ordering = ["student_number"]

    def __str__(self):
        return self.student_number


# ============================================================
# ACADEMIC YEAR & SEMESTER
# ============================================================

class AcademicYear(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="academic_years",
    )

    name = models.CharField(
        max_length=20,
        help_text="Example: 2026/2027",
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "academic_years"
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "name"],
                name="unique_academic_year_per_school",
            )
        ]

    def __str__(self):
        return self.name


class Semester(models.Model):

    SEMESTER_CHOICES = (
        (1, "Semester 1"),
        (2, "Semester 2"),
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="semesters",
    )

    number = models.PositiveSmallIntegerField(
        choices=SEMESTER_CHOICES,
    )

    name = models.CharField(
        max_length=50,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "semesters"
        ordering = ["academic_year", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_year", "number"],
                name="unique_semester_per_academic_year",
            )
        ]

    def __str__(self):
        return f"{self.academic_year.name} - {self.name}"


# ============================================================
# PROGRAM / STUDY PROGRAM
# ============================================================

class Program(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="programs",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=30,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "programs"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "code"],
                name="unique_program_code_per_school",
            )
        ]

    def __str__(self):
        return self.name


# ============================================================
# INTEREST CLASS / PEMINATAN
# ============================================================

class InterestClass(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="interest_classes",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=30,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "interest_classes"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "code"],
                name="unique_interest_class_code_per_school",
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


# ============================================================
# CLASS / ROMBEL
# ============================================================

class SchoolClass(models.Model):

    GRADE_CHOICES = (
        (10, "Grade 10"),
        (11, "Grade 11"),
        (12, "Grade 12"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("graduated", "Graduated"),
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="classes",
    )

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="classes",
    )

    interest_class = models.ForeignKey(
        InterestClass,
        on_delete=models.PROTECT,
        related_name="classes",
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=100,
        help_text="Example: IPS 2",
    )

    code = models.CharField(
        max_length=30,
        help_text="Example: IPS2",
    )

    grade_level = models.PositiveSmallIntegerField(
        choices=GRADE_CHOICES,
    )

    capacity = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "classes"
        ordering = ["grade_level", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_year", "code"],
                name="unique_class_code_per_academic_year",
            )
        ]

    def __str__(self):
        return f"{self.code} - Grade {self.grade_level}"


# ============================================================
# CLASS MEMBERSHIP
# ============================================================

class ClassMember(models.Model):

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name="members",
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="class_memberships",
    )

    joined_at = models.DateField(
        auto_now_add=True,
    )

    left_at = models.DateField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "class_members"
        constraints = [
            models.UniqueConstraint(
                fields=["school_class", "student"],
                name="unique_student_per_class",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.school_class}"


# ============================================================
# SUBJECT
# ============================================================

class SubjectGroup(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="subject_groups",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=30,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subject_groups"
        constraints = [
            models.UniqueConstraint(
                fields=["school", "code"],
                name="unique_subject_group_code_per_school",
            )
        ]

    def __str__(self):
        return self.name


class Subject(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="subjects",
    )

    subject_group = models.ForeignKey(
        SubjectGroup,
        on_delete=models.PROTECT,
        related_name="subjects",
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=30,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    passing_grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=75,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subjects"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "code"],
                name="unique_subject_code_per_school",
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


# ============================================================
# TEACHING ASSIGNMENT
# GURU + MAPEL + KELAS + TAHUN AJARAN + SEMESTER
# ============================================================

class TeachingAssignment(models.Model):

    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "teaching_assignments"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "teacher",
                    "subject",
                    "school_class",
                    "academic_year",
                    "semester",
                ],
                name="unique_teaching_assignment",
            )
        ]

    def __str__(self):
        return (
            f"{self.teacher} - "
            f"{self.subject} - "
            f"{self.school_class}"
        )


# ============================================================
# FILE MANAGEMENT
# ============================================================

class File(models.Model):

    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="uploaded_files",
    )

    file = models.FileField(
        upload_to="files/",
    )

    original_name = models.CharField(
        max_length=255,
    )

    file_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    file_size = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "files"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.original_name


# ============================================================
# LEARNING MATERIAL
# ============================================================

class Material(models.Model):

    teaching_assignment = models.ForeignKey(
        TeachingAssignment,
        on_delete=models.PROTECT,
        related_name="materials",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    text_content = models.TextField(
        blank=True,
        null=True,
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    is_published = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "materials"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class MaterialFile(models.Model):

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="files",
    )

    file = models.ForeignKey(
        File,
        on_delete=models.PROTECT,
        related_name="material_files",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "material_files"
        constraints = [
            models.UniqueConstraint(
                fields=["material", "file"],
                name="unique_material_file",
            )
        ]


# ============================================================
# ASSIGNMENT / TUGAS
# ============================================================

class Assignment(models.Model):

    teaching_assignment = models.ForeignKey(
        TeachingAssignment,
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    start_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    deadline = models.DateTimeField()

    max_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
    )

    is_published = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assignments"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class AssignmentFile(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="files",
    )

    file = models.ForeignKey(
        File,
        on_delete=models.PROTECT,
        related_name="assignment_files",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "assignment_files"
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "file"],
                name="unique_assignment_file",
            )
        ]


class AssignmentQuestion(models.Model):

    QUESTION_TYPE_CHOICES = (
        ("text", "Text"),
        ("multiple_choice", "Multiple Choice"),
        ("true_false", "True False"),
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question = models.TextField()

    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPE_CHOICES,
        default="text",
    )

    points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "assignment_questions"
        ordering = ["order"]


# ============================================================
# ASSIGNMENT SUBMISSION
# ============================================================

class AssignmentSubmission(models.Model):

    STATUS_CHOICES = (
        ("submitted", "Submitted"),
        ("late", "Late"),
        ("graded", "Graded"),
        ("returned", "Returned"),
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.PROTECT,
        related_name="submissions",
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="assignment_submissions",
    )

    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted",
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    feedback = models.TextField(
        blank=True,
        null=True,
    )

    graded_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assignment_submissions"
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="unique_submission_per_student",
            )
        ]

    def __str__(self):
        return f"{self.assignment} - {self.student}"


class SubmissionAnswer(models.Model):

    submission = models.ForeignKey(
        AssignmentSubmission,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        AssignmentQuestion,
        on_delete=models.PROTECT,
        related_name="answers",
    )

    answer_text = models.TextField(
        blank=True,
        null=True,
    )

    is_correct = models.BooleanField(
        blank=True,
        null=True,
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "submission_answers"
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "question"],
                name="unique_answer_per_question",
            )
        ]


class SubmissionFile(models.Model):

    submission = models.ForeignKey(
        AssignmentSubmission,
        on_delete=models.CASCADE,
        related_name="files",
    )

    file = models.ForeignKey(
        File,
        on_delete=models.PROTECT,
        related_name="submission_files",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "submission_files"
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "file"],
                name="unique_submission_file",
            )
        ]


# ============================================================
# ASSESSMENT / PENILAIAN
# ============================================================

class Assessment(models.Model):

    ASSESSMENT_TYPE_CHOICES = (
        ("daily", "Daily"),
        ("assignment", "Assignment"),
        ("quiz", "Quiz"),
        ("midterm", "Midterm"),
        ("final", "Final"),
        ("project", "Project"),
        ("other", "Other"),
    )

    teaching_assignment = models.ForeignKey(
        TeachingAssignment,
        on_delete=models.PROTECT,
        related_name="assessments",
    )

    title = models.CharField(
        max_length=255,
    )

    assessment_type = models.CharField(
        max_length=20,
        choices=ASSESSMENT_TYPE_CHOICES,
    )

    assessment_date = models.DateField()

    max_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assessments"
        ordering = ["-assessment_date"]

    def __str__(self):
        return self.title


class AssessmentItem(models.Model):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="items",
    )

    question = models.TextField()

    points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "assessment_items"
        ordering = ["order"]


class Grade(models.Model):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.PROTECT,
        related_name="grades",
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="grades",
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    feedback = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "grades"
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "student"],
                name="unique_grade_per_student",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.score}"


# ============================================================
# GRADE COMPONENT
# ============================================================

class GradeComponent(models.Model):

    teaching_assignment = models.ForeignKey(
        TeachingAssignment,
        on_delete=models.PROTECT,
        related_name="grade_components",
    )

    name = models.CharField(
        max_length=100,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "grade_components"

    def __str__(self):
        return self.name


# ============================================================
# REPORT CARD
# ============================================================

class ReportCard(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("locked", "Locked"),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="report_cards",
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name="report_cards",
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="report_cards",
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="report_cards",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "report_cards"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_year",
                    "semester",
                ],
                name="unique_report_card_per_semester",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.semester}"


# ============================================================
# SCHEDULE
# ============================================================

class Schedule(models.Model):

    DAY_CHOICES = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )

    teaching_assignment = models.ForeignKey(
        TeachingAssignment,
        on_delete=models.PROTECT,
        related_name="schedules",
    )

    day_of_week = models.PositiveSmallIntegerField(
        choices=DAY_CHOICES,
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    room = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "schedules"
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return (
            f"{self.teaching_assignment} - "
            f"{self.start_time} - {self.end_time}"
        )


# ============================================================
# SCHOOL ATTENDANCE
# ABSENSI MASUK SEKOLAH
# ============================================================

class SchoolAttendanceSession(models.Model):

    date = models.DateField()

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name="school_attendance_sessions",
    )

    start_time = models.TimeField(
        blank=True,
        null=True,
    )

    end_time = models.TimeField(
        blank=True,
        null=True,
    )

    is_open = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "school_attendance_sessions"
        constraints = [
            models.UniqueConstraint(
                fields=["school", "date"],
                name="unique_school_attendance_per_day",
            )
        ]

    def __str__(self):
        return f"{self.school} - {self.date}"


class SchoolAttendanceRecord(models.Model):

    STATUS_CHOICES = (
        ("present", "Present"),
        ("late", "Late"),
        ("absent", "Absent"),
        ("excused", "Excused"),
        ("sick", "Sick"),
    )

    session = models.ForeignKey(
        SchoolAttendanceSession,
        on_delete=models.CASCADE,
        related_name="records",
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="school_attendance_records",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    check_in_time = models.DateTimeField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "school_attendance_records"
        constraints = [
            models.UniqueConstraint(
                fields=["session", "student"],
                name="unique_school_attendance_student",
            )
        ]


# ============================================================
# CLASS ATTENDANCE
# ABSENSI SAAT MASUK KELAS / MAPEL
# ============================================================

class ClassAttendanceSession(models.Model):

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.PROTECT,
        related_name="attendance_sessions",
    )

    date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    is_open = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "class_attendance_sessions"
        constraints = [
            models.UniqueConstraint(
                fields=["schedule", "date"],
                name="unique_class_attendance_session",
            )
        ]

    def __str__(self):
        return f"{self.schedule} - {self.date}"


class ClassAttendanceRecord(models.Model):

    STATUS_CHOICES = (
        ("present", "Present"),
        ("late", "Late"),
        ("absent", "Absent"),
        ("excused", "Excused"),
        ("sick", "Sick"),
    )

    session = models.ForeignKey(
        ClassAttendanceSession,
        on_delete=models.CASCADE,
        related_name="records",
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.PROTECT,
        related_name="class_attendance_records",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    check_in_time = models.DateTimeField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "class_attendance_records"
        constraints = [
            models.UniqueConstraint(
                fields=["session", "student"],
                name="unique_class_attendance_student",
            )
        ]


# ============================================================
# ANNOUNCEMENT
# BISA UNTUK DASHBOARD + LANDING PAGE
# ============================================================

class Announcement(models.Model):

    TARGET_CHOICES = (
        ("public", "Public"),
        ("internal", "Internal"),
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("all", "All"),
    )

    title = models.CharField(
        max_length=255,
    )

    content = models.TextField()

    target = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        default="internal",
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    is_published = models.BooleanField(
        default=False,
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="created_announcements",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "announcements"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ============================================================
# NOTIFICATION
# ============================================================

class Notification(models.Model):
    TYPE_CHOICES = (
        ("announcement", "Announcement"),
        ("assignment", "Assignment"),
        ("grade", "Grade"),
        ("attendance", "Attendance"),
        ("system", "System"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
    )

    title = models.CharField(
        max_length=255,
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False,
    )

    read_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ============================================================
# COMMUNICATION
# ============================================================

class Conversation(models.Model):

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="created_conversations",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "conversations"


class ConversationMember(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="members",
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="conversations",
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "conversation_members"
        constraints = [
            models.UniqueConstraint(
                fields=["conversation", "user"],
                name="unique_conversation_member",
            )
        ]


class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="sent_messages",
    )

    message = models.TextField()

    sent_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "messages"
        ordering = ["sent_at"]


# ============================================================
# SYSTEM SETTINGS
# ============================================================

class Setting(models.Model):

    key = models.CharField(
        max_length=100,
        unique=True,
    )

    value = models.TextField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "settings"

    def __str__(self):
        return self.key


# ============================================================
# ACTIVITY LOG
# ============================================================

class ActivityLog(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
    )

    action = models.CharField(
        max_length=100,
    )

    model_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "activity_logs"
        ordering = ["-created_at"]


# ============================================================
# AUDIT LOG
# ============================================================

class AuditLog(models.Model):

    ACTION_CHOICES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("restore", "Restore"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
    )

    model_name = models.CharField(
        max_length=100,
    )

    object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )

    old_data = models.JSONField(
        blank=True,
        null=True,
    )

    new_data = models.JSONField(
        blank=True,
        null=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]