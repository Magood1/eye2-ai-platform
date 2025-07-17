# apps/diagnosis/models.py
import uuid
from django.db import models
from django.conf import settings
from apps.users.models import Patient 


class ModelVersion(models.Model):
    """يخزن معلومات حول إصدارات نماذج الذكاء الاصطناعي المستخدمة."""
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    file_path = models.CharField(max_length=255, help_text="Path to the model file")
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - v{self.version}"

class Diagnosis(models.Model):
    """يسجل طلب تشخيص كامل، من الإدخال إلى النتيجة."""
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        SUCCESS = "SUCCESS", "Success"
        FAILURE = "FAILURE", "Failure"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name="diagnoses", null=True) # سيتم بناء Patient في Sprint 3
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="diagnoses")
    physician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="diagnoses")

    # مُدخلات
    left_fundus_image = models.ImageField(upload_to='diagnoses/images/%Y/%m/%d/')
    right_fundus_image = models.ImageField(upload_to='diagnoses/images/%Y/%m/%d/')

    # تتبع الحالة
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    
    # النتائج
    result = models.JSONField(null=True, blank=True, help_text="Stores the final JSON output from the AI pipeline")
    error_message = models.TextField(null=True, blank=True)

    # معلومات التدقيق
    model_version = models.ForeignKey(ModelVersion, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diagnosis {self.id} - {self.status}"
    
    def get_clinic(self):
        """دالة مساعدة لجلب العيادة المرتبطة بهذا التشخيص عبر المريض."""
        return self.patient.clinic if self.patient else None
