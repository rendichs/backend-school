from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Prodi, BiodataGuru, BiodataMurid, 
    Kelas, Materi, SesiAbsensi, KehadiranMurid, 
    Tugas, PengumpulanTugas
)

# Mendaftarkan CustomUser dengan UserAdmin agar fitur hashing password bawaan Django tetap berfungsi
admin.site.register(CustomUser, UserAdmin)

# Mendaftarkan model data master dan operasional
admin.site.register(Prodi)
admin.site.register(BiodataGuru)
admin.site.register(BiodataMurid)
admin.site.register(Kelas)
admin.site.register(Materi)
admin.site.register(SesiAbsensi)
admin.site.register(KehadiranMurid)
admin.site.register(Tugas)
admin.site.register(PengumpulanTugas)