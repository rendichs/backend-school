from rest_framework import serializers
from .models import CustomUser, Prodi, Kelas, Tugas, Materi, BiodataGuru, BiodataMurid

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

class TeacherSerializer(serializers.ModelSerializer):
    nip = serializers.CharField(source="biodata_guru.nip")
    jantina = serializers.CharField(source="biodata_guru.jantina")
    no_telefon = serializers.CharField(
        source="biodata_guru.no_telefon",
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    alamat = serializers.CharField(
        source="biodata_guru.alamat",
        required=False,
        allow_blank=True,
        allow_null=True,
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
            "nama_lengkap",
            "role",
            "nip",
            "jantina",
            "no_telefon",
            "alamat",
            "is_active",
        ]

        read_only_fields = ["id", "role"]

    def create(self, validated_data):
        biodata_data = validated_data.pop("biodata_guru")
        password = validated_data.pop("password", None)

        user = CustomUser(
            **validated_data,
            role="guru",
        )

        if password:
            user.set_password(password)
        else:
            raise serializers.ValidationError({
                "password": "Password wajib diisi."
            })

        user.save()

        BiodataGuru.objects.create(
            user=user,
            **biodata_data,
        )

        return user

# (Anda bisa menambahkan serializer untuk Materi, Biodata, dan Absensi dengan pola yang sama)