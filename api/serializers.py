from rest_framework import serializers
from .models import CustomUser, Prodi, Kelas, Tugas, Materi, BiodataGuru, BiodataMurid
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer

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
    nip = serializers.CharField(
        source="biodata_guru.nip"
    )

    jantina = serializers.CharField(
        source="biodata_guru.jantina"
    )

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

        read_only_fields = [
            "id",
            "role",
        ]

    def create(self, validated_data):
        biodata_data = validated_data.pop(
            "biodata_guru"
        )

        password = validated_data.pop(
            "password",
            None
        )

        if not password:
            raise serializers.ValidationError({
                "password": "Password wajib diisi."
            })

        user = CustomUser(
            **validated_data,
            role="guru",
        )

        user.set_password(password)
        user.save()

        BiodataGuru.objects.create(
            user=user,
            **biodata_data,
        )

        return user

    def update(self, instance, validated_data):
        biodata_data = validated_data.pop(
            "biodata_guru",
            {}
        )

        password = validated_data.pop(
            "password",
            None
        )

        # Update user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update password jika diisi
        if password:
            instance.set_password(password)

        instance.save()

        # Update biodata
        biodata = instance.biodata_guru

        for attr, value in biodata_data.items():
            setattr(biodata, attr, value)

        biodata.save()

        return instance

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

        # Cek apakah akun ada tetapi sedang nonaktif
        inactive_user = CustomUser.objects.filter(
            username=username
        ).first()

        if inactive_user and not inactive_user.is_active:
            raise serializers.ValidationError({
                "detail": (
                    "Akun Anda sedang dinonaktifkan. "
                    "Silakan hubungi administrator!"
                )
            })

        raise serializers.ValidationError({
            "detail": "Username atau password salah."
        })