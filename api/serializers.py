from rest_framework import serializers
from .models import CustomUser, Prodi, Kelas, Tugas, Materi

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'nama_lengkap']

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prodi
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tugas
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materi
        fields = '__all__'

# (Anda bisa menambahkan serializer untuk Materi, Biodata, dan Absensi dengan pola yang sama)