from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Prodi, Kelas, Tugas
from .serializers import UserSerializer, ProdiSerializer, KelasSerializer, TugasSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] # API hanya bisa diakses jika menyertakan Token valid

class ProdiViewSet(viewsets.ModelViewSet):
    queryset = Prodi.objects.all()
    serializer_class = ProdiSerializer

class KelasViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.all()
    serializer_class = KelasSerializer

class TugasViewSet(viewsets.ModelViewSet):
    queryset = Tugas.objects.all()
    serializer_class = TugasSerializer