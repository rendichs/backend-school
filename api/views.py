from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Prodi, Kelas, Tugas, Materi, BiodataGuru
from .serializers import UserSerializer, MajorSerializer, ClassSerializer, AssignmentSerializer, MaterialSerializer, GuruSerializer
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
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'role': user.role, # Mengirim role ke frontend
            'user_id': user.pk,
            'nama_lengkap': user.nama_lengkap
        })

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Materi.objects.all()
    serializer_class = MaterialSerializer

class GuruViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role="guru")
    serializer_class = GuruSerializer
    permission_classes = [IsAdminUserRole]