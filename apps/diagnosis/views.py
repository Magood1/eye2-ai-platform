# apps/diagnosis/views.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Diagnosis
from .serializers import DiagnosisCreateSerializer, DiagnosisDetailSerializer
from .tasks import process_diagnosis
from apps.users.models import Patient
from apps.diagnosis import serializers

from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')



class DiagnosisViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    ViewSet لإنشاء واسترجاع التشخيصات.
    - POST: ينشئ طلب تشخيص ويطلق مهمة في الخلفية.
    - GET: يسترجع حالة ونتيجة طلب معين.
    """
    queryset = Diagnosis.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return DiagnosisCreateSerializer
        return DiagnosisDetailSerializer

    def perform_create(self, serializer):
        """
        يحفظ السجل المبدئي ويطلق مهمة Celery غير المتزامنة.
        يحفظ السجل ويربطه بالمريض والطبيب الحالي.
        """
        patient_id = serializer.validated_data.pop('patient_id')
        try:
            # تحقق من أن الطبيب لديه صلاحية على هذا المريض
            patient = self.request.user.patients.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("You do not have permission for this patient.")

        diagnosis = serializer.save(
            patient=patient,
            physician=self.request.user
        )
        # إطلاق المهمة غير المتزامنة
        process_diagnosis.delay(diagnosis_id=str(diagnosis.id))