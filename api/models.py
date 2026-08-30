from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username wajib diisi")
            
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # SISTEM OTOMATIS: Memaksa role menjadi admin 
        # setiap kali perintah createsuperuser dijalankan
        extra_fields.setdefault('role', 'admin')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('guru', 'Guru'),
        ('murid', 'Murid'),
    )
    # Aturan dasar untuk pendaftar umum
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='murid')
    nama_lengkap = models.CharField(max_length=255, blank=True, null=True)

    objects = CustomUserManager()

# ==================== DATA MASTER ====================

class Prodi(models.Model):
    nama_prodi = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_prodi

class BiodataGuru(models.Model):
    # Relasi One-to-One: 1 akun user hanya punya 1 biodata guru
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'guru'})
    nip = models.CharField(max_length=50, unique=True)
    jantina = models.CharField(max_length=15, choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')])
    no_telefon = models.CharField(max_length=20, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nip

class BiodataMurid(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'murid'})
    nis = models.CharField(max_length=50, unique=True)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True)
    jantina = models.CharField(max_length=15, choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')])
    tarikh_lahir = models.DateField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nis

# ==================== MANAJEMEN KELAS & KONTEN ====================

class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=100)
    tingkat = models.CharField(max_length=20)
    prodi = models.ForeignKey(Prodi, on_delete=models.CASCADE)
    guru = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'guru'})

    def __str__(self):
        return f"{self.nama_kelas} - {self.tingkat}"

class Materi(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    judul = models.CharField(max_length=255)
    file_materi = models.FileField(upload_to='materi/', blank=True, null=True)
    teks_materi = models.TextField(blank=True, null=True)
    waktu_dibuat = models.DateTimeField(auto_now_add=True)

# ==================== INTERAKSI DARING (ABSENSI & TUGAS) ====================

class SesiAbsensi(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    waktu_mulai = models.DateTimeField()
    waktu_selesai = models.DateTimeField()

class KehadiranMurid(models.Model):
    sesi_absensi = models.ForeignKey(SesiAbsensi, on_delete=models.CASCADE)
    murid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'murid'})
    waktu_absen = models.DateTimeField(auto_now_add=True)

class Tugas(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    judul_tugas = models.CharField(max_length=255)
    deskripsi = models.TextField()
    deadline = models.DateTimeField()

class PengumpulanTugas(models.Model):
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE)
    murid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'murid'})
    file_hasil = models.FileField(upload_to='tugas_hasil/')
    waktu_submit = models.DateTimeField(auto_now_add=True)
    nilai = models.IntegerField(blank=True, null=True)