from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    CustomUser,
    Prodi,
    Kelas,
    Tugas,
    Materi,
    BiodataGuru,
)

from .serializers import (
    UserSerializer,
    MajorSerializer,
    ClassSerializer,
    AssignmentSerializer,
    MaterialSerializer,
    TeacherSerializer,
    CustomAuthTokenSerializer,
)

from .permissions import IsAdminUserRole


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] # API hanya bisa diakses jika menyertakan Token valid

class MajorViewSet(viewsets.ModelViewSet):
    queryset = Prodi.objects.all()
    serializer_class = MajorSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.all()
    serializer_class = ClassSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Tugas.objects.all()
    serializer_class = AssignmentSerializer

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "role": user.role,
                "user_id": user.pk,
                "nama_lengkap": user.nama_lengkap,
            }
        )

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Materi.objects.all()
    serializer_class = MaterialSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = (
        CustomUser.objects
        .filter(role="guru")
        .select_related("biodata_guru")
    )

    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUserRole]

    def destroy(self, request, *args, **kwargs):
        teacher = self.get_object()

        # ==================================================
        # FIREWALL PENGHAPUSAN GURU
        # ==================================================

        # Cek apakah guru masih digunakan sebagai pengajar kelas
        jumlah_kelas = Kelas.objects.filter(
            guru=teacher
        ).count()

        if jumlah_kelas > 0:
            return Response(
                {
                    "detail": (
                        f"Guru {teacher.nama_lengkap} tidak dapat dihapus "
                        f"karena masih digunakan pada {jumlah_kelas} kelas."
                    ),
                    "code": "teacher_in_use",
                    "dependencies": {
                        "kelas": jumlah_kelas,
                    },
                },
                status=status.HTTP_409_CONFLICT,
            )

        # ==================================================
        # JIKA AMAN → LANJUTKAN DELETE
        # ==================================================

        return super().destroy(
            request,
            *args,
            **kwargs
        )