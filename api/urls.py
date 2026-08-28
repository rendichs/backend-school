from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MajorViewSet, ClassViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'majors', MajorViewSet)       # Sebelumnya: prodi
router.register(r'classes', ClassViewSet)      # Sebelumnya: kelas
router.register(r'assignments', AssignmentViewSet)  # Sebelumnya: tugas

urlpatterns = [
    path('', include(router.urls)),
]