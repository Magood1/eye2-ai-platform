# apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, UserProfileView,  ClinicViewSet, PatientViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'clinics', ClinicViewSet)
router.register(r'patients', PatientViewSet)



urlpatterns = [
    # نقاط نهاية المصادقة
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('', include(router.urls)), # إضافة مسارات العيادات والمرضى

    # نقاط نهاية JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
