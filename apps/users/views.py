# apps/users/views.py
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer, UserSerializer, ClinicSerializer, PatientSerializer
from .models import User,  Clinic, Patient
from .permissions import IsAdmin, IsAssignedDoctorOrReadOnly, IsDoctor
from apps.core.audit import log_patient_access
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Register a new user (Doctor or Admin)",
    description="Creates a new user account. Any user can register."
)
class UserRegisterView(generics.CreateAPIView):
    """عرض API لتسجيل مستخدم جديد."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # أي شخص يمكنه التسجيل
    serializer_class = UserRegisterSerializer

class UserProfileView(generics.RetrieveAPIView):
    """
    عرض API محمي لجلب ملف تعريف المستخدم المسجل دخوله.
    هذا endpoint مثالي لاختبار صلاحيات JWT.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    

class ClinicViewSet(viewsets.ModelViewSet):
    """ViewSet لإدارة العيادات. الوصول مقيد للمسؤولين."""
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    #permission_classes = [IsAdmin, IsDoctor] # فقط المسؤول يمكنه إدارة العيادات

class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet لإدارة المرضى."""
    queryset = Patient.objects.all()    # ← هذه السطر ضروري

    serializer_class = PatientSerializer
    permission_classes = [IsAssignedDoctorOrReadOnly]

    def get_queryset(self):
        """
        - المسؤولون يرون جميع المرضى.
        - الأطباء يرون فقط المرضى المرتبطين بهم.
        """
        user = self.request.user
        if user.role == User.Roles.ADMIN:
            return Patient.objects.all()
        return user.patients.all() # استرجاع المرضى المرتبطين بالطبيب
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        log_patient_access(request.user, instance, "retrieved")
        return super().retrieve(request, *args, **kwargs)