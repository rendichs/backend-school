from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProdiViewSet, KelasViewSet, TugasViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'prodi', ProdiViewSet)
router.register(r'kelas', KelasViewSet)
router.register(r'tugas', TugasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]